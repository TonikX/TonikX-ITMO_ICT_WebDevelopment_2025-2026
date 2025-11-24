package io.github.artsobol.kurkod.common.util;

import io.github.artsobol.kurkod.common.exception.VersionConflictException;
import io.github.artsobol.kurkod.web.domain.common.error.VersionError;
import lombok.extern.slf4j.Slf4j;

import java.util.Objects;

@Slf4j
public final class VersionUtils {

    private VersionUtils() {}

    public static void checkVersion(Long entityVersion, Long requestVersion) {
        if (!Objects.equals(entityVersion, requestVersion)) {
            log.info(VersionError.VERSION_NOT_EQUALS.format(entityVersion, requestVersion));
            throw new VersionConflictException(VersionError.VERSION_NOT_EQUALS, requestVersion, entityVersion);
        }
    }
}
