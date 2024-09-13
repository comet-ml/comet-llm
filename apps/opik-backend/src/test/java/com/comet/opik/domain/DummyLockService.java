package com.comet.opik.domain;

import com.comet.opik.infrastructure.redis.LockService;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public class DummyLockService implements LockService {

    @Override
    public <T> Mono<T> executeWithLock(LockService.Lock lock, Mono<T> action) {
        return action;
    }

    @Override
    public <T> Flux<T> executeWithLock(LockService.Lock lock, Flux<T> action) {
        return action;
    }
}