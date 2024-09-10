package com.comet.opik.domain;

import com.comet.opik.api.ExperimentItem;
import com.comet.opik.infrastructure.auth.RequestContext;
import com.google.common.base.Preconditions;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import jakarta.ws.rs.ClientErrorException;
import jakarta.ws.rs.NotFoundException;
import jakarta.ws.rs.core.Response;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import reactor.core.publisher.Mono;

import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

@Singleton
@RequiredArgsConstructor(onConstructor_ = @Inject)
@Slf4j
public class ExperimentItemService {

    private final @NonNull ExperimentItemDAO experimentItemDAO;
    private final @NonNull ExperimentService experimentService;
    private final @NonNull DatasetItemDAO datasetItemDAO;

    public Mono<Void> create(Set<ExperimentItem> experimentItems) {
        Preconditions.checkArgument(CollectionUtils.isNotEmpty(experimentItems),
                "Argument 'experimentItems' must not be empty");

        return Mono.deferContextual(ctx -> {
            String workspaceId = ctx.get(RequestContext.WORKSPACE_ID);

            var experimentItemsWithValidIds = addIdIfAbsentAndValidateIt(experimentItems, workspaceId);

            log.info("Creating experiment items, count '{}'", experimentItemsWithValidIds.size());
            return experimentItemDAO.insert(experimentItemsWithValidIds)
                    .then();
        });
    }

    private Set<ExperimentItem> addIdIfAbsentAndValidateIt(Set<ExperimentItem> experimentItems, String workspaceId) {
        validateExperimentsWorkspace(experimentItems, workspaceId);

        validateDatasetItemsWorkspace(experimentItems, workspaceId);

        return experimentItems.stream()
                .map(item -> {
                    IdGenerator.validateVersion(item.id(), "Experiment Item");
                    IdGenerator.validateVersion(item.experimentId(), "Experiment Item experiment");
                    IdGenerator.validateVersion(item.datasetItemId(), "Experiment Item datasetItem");
                    IdGenerator.validateVersion(item.traceId(), "Experiment Item trace");
                    return item;
                })
                .collect(Collectors.toUnmodifiableSet());
    }

    private void validateExperimentsWorkspace(Set<ExperimentItem> experimentItems, String workspaceId) {
        Set<UUID> experimentIds = experimentItems
                .stream()
                .map(ExperimentItem::experimentId)
                .collect(Collectors.toSet());

        boolean allExperimentsBelongToWorkspace = Boolean.TRUE
                .equals(experimentService.validateExperimentWorkspace(workspaceId, experimentIds)
                        .block());

        if (!allExperimentsBelongToWorkspace) {
            throw new ClientErrorException(
                    "Upserting experiment item with 'experiment_id' not belonging to the workspace",
                    Response.Status.CONFLICT);
        }
    }

    private void validateDatasetItemsWorkspace(Set<ExperimentItem> experimentItems, String workspaceId) {
        Set<UUID> datasetItemIds = experimentItems
                .stream()
                .map(ExperimentItem::datasetItemId)
                .collect(Collectors.toSet());

        boolean allDatasetItemsBelongToWorkspace = Boolean.TRUE
                .equals(validateDatasetItemWorkspace(workspaceId, datasetItemIds)
                        .contextWrite(ctx -> ctx.put(RequestContext.WORKSPACE_ID, workspaceId))
                        .block());

        if (!allDatasetItemsBelongToWorkspace) {
            throw new ClientErrorException(
                    "Upserting experiment item with 'dataset_item_id' not belonging to the workspace",
                    Response.Status.CONFLICT);
        }
    }

    private Mono<Boolean> validateDatasetItemWorkspace(String workspaceId, Set<UUID> datasetItemIds) {
        if (datasetItemIds.isEmpty()) {
            return Mono.just(true);
        }

        return datasetItemDAO.getDatasetItemWorkspace(datasetItemIds)
                .map(datasetItemWorkspace -> datasetItemWorkspace.stream()
                        .allMatch(datasetItem -> workspaceId.equals(datasetItem.workspaceId())));
    }

    public Mono<ExperimentItem> get(@NonNull UUID id) {
        log.info("Getting experiment item by id '{}'", id);
        return experimentItemDAO.get(id)
                .switchIfEmpty(Mono.error(newNotFoundException(id)));
    }

    private NotFoundException newNotFoundException(UUID id) {
        return new NotFoundException("Not found experiment item with id '%s'".formatted(id));
    }

    public Mono<Void> delete(@NonNull Set<UUID> ids) {
        Preconditions.checkArgument(CollectionUtils.isNotEmpty(ids),
                "Argument 'ids' must not be empty");

        log.info("Deleting experiment items, count '{}'", ids.size());
        return experimentItemDAO.delete(ids).then();
    }

}
