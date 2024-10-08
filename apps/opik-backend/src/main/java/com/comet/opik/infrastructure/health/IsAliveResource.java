package com.comet.opik.infrastructure.health;

import com.codahale.metrics.health.HealthCheck;
import com.codahale.metrics.health.HealthCheckRegistry;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import lombok.RequiredArgsConstructor;

@Path("/is-alive")
@Produces(MediaType.APPLICATION_JSON)
@RequiredArgsConstructor(onConstructor_ = @Inject)
public class IsAliveResource {

    private final HealthCheckRegistry registry;

    public record IsAliveResponse(String message, boolean healthy) {

        static IsAliveResponse healthy(String message) {
            return new IsAliveResponse(message, true);
        }

        static IsAliveResponse unhealthy(String message) {
            return new IsAliveResponse(message, false);
        }
    }

    @GET
    @Path("/ping")
    public Response isAlive() {

        var isServerAlive = registry.runHealthChecks()
                .values()
                .stream()
                .filter(result -> !result.isHealthy())
                .allMatch(HealthCheck.Result::isHealthy);

        if (isServerAlive) {
            return Response.ok(IsAliveResponse.healthy("Healthy Server")).build();
        } else {
            return Response.serverError().entity(IsAliveResponse.unhealthy("Not Healthy")).build();
        }
    }
}
