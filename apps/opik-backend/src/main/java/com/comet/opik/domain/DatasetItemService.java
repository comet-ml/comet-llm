package com.comet.opik.domain;

import com.clickhouse.client.ClickHouseException;
import com.comet.opik.api.Dataset;
import com.comet.opik.api.DatasetItem;
import com.comet.opik.api.DatasetItemBatch;
import com.comet.opik.api.DatasetItemSearchCriteria;
import com.comet.opik.api.error.ErrorMessage;
import com.comet.opik.api.error.IdentifierMismatchException;
import com.comet.opik.infrastructure.auth.RequestContext;
import com.google.inject.ImplementedBy;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import jakarta.ws.rs.ClientErrorException;
import jakarta.ws.rs.NotFoundException;
import jakarta.ws.rs.core.Response;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import static com.comet.opik.api.DatasetItem.DatasetItemPage;

@ImplementedBy(DatasetItemServiceImpl.class)
public interface DatasetItemService {

    Mono<Void> save(DatasetItemBatch batch);

    Mono<DatasetItem> get(UUID id);

    Mono<Void> delete(List<UUID> ids);

    Mono<DatasetItemPage> getItems(UUID datasetId, int page, int size);

    Mono<DatasetItemPage> getItems(int page, int size, DatasetItemSearchCriteria datasetItemSearchCriteria);

    Flux<DatasetItem> getItems(UUID datasetId, int limit, UUID lastRetrievedId);
}

@Singleton
@RequiredArgsConstructor(onConstructor_ = @Inject)
@Slf4j
class DatasetItemServiceImpl implements DatasetItemService {

    private final @NonNull DatasetItemDAO dao;
    private final @NonNull DatasetService datasetService;
    private final @NonNull TraceService traceService;
    private final @NonNull SpanService spanService;

    @Override
    public Mono<Void> save(@NonNull DatasetItemBatch batch) {
        if (batch.datasetId() == null && batch.datasetName() == null) {
            return Mono.error(failWithError("dataset_id or dataset_name must be provided"));
        }

        return getDatasetId(batch)
                .flatMap(it -> saveBatch(batch, it))
                .onErrorResume(this::tryHandlingException)
                .then();
    }

    private Mono<UUID> getDatasetId(DatasetItemBatch batch) {
        return Mono.deferContextual(ctx -> {
            String userName = ctx.get(RequestContext.USER_NAME);
            String workspaceId = ctx.get(RequestContext.WORKSPACE_ID);

            return Mono.fromCallable(() -> {

                if (batch.datasetId() == null) {
                    return datasetService.getOrCreate(workspaceId, batch.datasetName(), userName);
                }

                Dataset dataset = datasetService.findById(batch.datasetId(), workspaceId);

                if (dataset == null) {
                    throw throwsConflict(
                            "workspace_name from dataset item batch and dataset_id from item does not match");
                }

                return dataset.id();
            }).subscribeOn(Schedulers.boundedElastic());
        });
    }

    private Throwable failWithError(String error) {
        return new ClientErrorException(Response.status(422).entity(new ErrorMessage(List.of(error))).build());
    }

    private ClientErrorException throwsConflict(String error) {
        return new ClientErrorException(Response.status(409).entity(new ErrorMessage(List.of(error))).build());
    }

    @Override
    public Mono<DatasetItem> get(@NonNull UUID id) {
        return dao.get(id)
                .switchIfEmpty(Mono.defer(() -> Mono.error(failWithNotFound("Dataset item not found"))));
    }

    @Override
    public Flux<DatasetItem> getItems(@NonNull UUID datasetId, int limit, UUID lastRetrievedId) {
        return dao.getItems(datasetId, limit, lastRetrievedId);
    }

    private Mono<Long> saveBatch(DatasetItemBatch batch, UUID id) {
        if (batch.items().isEmpty()) {
            return Mono.empty();
        }

        List<DatasetItem> items = addIdIfAbsent(batch);

        return Mono.deferContextual(ctx -> {

            String workspaceId = ctx.get(RequestContext.WORKSPACE_ID);

            return validateSpans(workspaceId, items)
                    .then(Mono.defer(() -> validateTraces(workspaceId, items)))
                    .then(Mono.defer(() -> dao.save(id, items)));
        });
    }

    private Mono<Void> validateSpans(String workspaceId, List<DatasetItem> items) {
        Set<UUID> spanIds = items.stream()
                .map(DatasetItem::spanId)
                .filter(Objects::nonNull)
                .collect(Collectors.toSet());

        return spanService.validateSpanWorkspace(workspaceId, spanIds)
                .flatMap(valid -> {
                    if (Boolean.FALSE.equals(valid)) {
                        return failWithConflict("span workspace and dataset item workspace does not match");
                    }

                    return Mono.empty();
                });
    }

    private Mono<Boolean> validateTraces(String workspaceId, List<DatasetItem> items) {
        Set<UUID> traceIds = items.stream()
                .map(DatasetItem::traceId)
                .filter(Objects::nonNull)
                .collect(Collectors.toSet());

        return traceService.validateTraceWorkspace(workspaceId, traceIds)
                .flatMap(valid -> {
                    if (Boolean.FALSE.equals(valid)) {
                        return failWithConflict("trace workspace and dataset item workspace does not match");
                    }

                    return Mono.empty();
                });
    }

    private List<DatasetItem> addIdIfAbsent(DatasetItemBatch batch) {
        return batch.items()
                .stream()
                .map(item -> {
                    IdGenerator.validateVersion(item.id(), "dataset_item");
                    return item;
                })
                .toList();
    }

    private Mono<Long> tryHandlingException(Throwable e) {
        return switch (e) {
            case ClickHouseException clickHouseException -> {
                //TODO: Find a better way to handle this.
                // This is a workaround to handle the case when project_id from score and project_name from project does not match.
                if (clickHouseException.getMessage().contains("TOO_LARGE_STRING_SIZE") &&
                        clickHouseException.getMessage().contains("_CAST(dataset_id, FixedString(36)")) {
                    yield failWithConflict(
                            "dataset_name or dataset_id from dataset item batch and dataset_id from item does not match");
                }

                if (clickHouseException.getMessage().contains("TOO_LARGE_STRING_SIZE") &&
                        clickHouseException.getMessage().contains("_CAST(workspace_id, FixedString(36))")) {
                    yield failWithConflict(
                            "workspace_name from dataset item does not match");
                }
                yield Mono.error(e);
            }
            default -> Mono.error(e);
        };
    }

    private <T> Mono<T> failWithConflict(String message) {
        return Mono.error(new IdentifierMismatchException(new ErrorMessage(List.of(message))));
    }

    private NotFoundException failWithNotFound(String message) {
        return new NotFoundException(message,
                Response.status(Response.Status.NOT_FOUND).entity(new ErrorMessage(List.of(message))).build());
    }

    @Override
    public Mono<Void> delete(@NonNull List<UUID> ids) {
        if (ids.isEmpty()) {
            return Mono.empty();
        }

        return dao.delete(ids).then();
    }

    @Override
    public Mono<DatasetItemPage> getItems(@NonNull UUID datasetId, int page, int size) {
        return dao.getItems(datasetId, page, size);
    }

    @Override
    public Mono<DatasetItemPage> getItems(
            int page, int size, @NonNull DatasetItemSearchCriteria datasetItemSearchCriteria) {
        log.info("Finding dataset items with experiment items by '{}', page '{}', size '{}'",
                datasetItemSearchCriteria, page, size);
        return dao.getItems(datasetItemSearchCriteria, page, size);
    }
}
