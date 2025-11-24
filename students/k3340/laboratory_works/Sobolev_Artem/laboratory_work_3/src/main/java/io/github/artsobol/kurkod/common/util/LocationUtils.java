package io.github.artsobol.kurkod.common.util;

import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;

public final class LocationUtils {

    private LocationUtils() {}

    public static URI buildLocation(int id) {
        return ServletUriComponentsBuilder
                .fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(id)
                .toUri();
    }

    public static URI buildLocation(Long id) {
        return ServletUriComponentsBuilder
                .fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(id)
                .toUri();
    }

    public static URI buildLocation() {
        return ServletUriComponentsBuilder
                .fromCurrentRequest()
                .build()
                .toUri();
    }

    public static URI buildLocation(Long workerId, Long dismissedId) {
        return ServletUriComponentsBuilder
                .fromCurrentContextPath()
                .path("/api/v1/dismissals/workers/{workerId}/dismissed/{dismissedId}")
                .buildAndExpand(workerId, dismissedId)
                .toUri();
    }

    public static URI buildLocation(String pathTemplate, Object... uriVars) {
        return ServletUriComponentsBuilder
                .fromCurrentContextPath()
                .path(pathTemplate)
                .buildAndExpand(uriVars)
                .toUri();
    }
}
