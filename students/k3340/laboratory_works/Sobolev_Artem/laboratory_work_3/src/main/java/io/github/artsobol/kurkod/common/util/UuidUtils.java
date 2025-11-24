package io.github.artsobol.kurkod.common.util;

import io.github.artsobol.kurkod.common.constants.CommonConstants;
import io.github.artsobol.kurkod.common.constants.PasswordConstants;

import java.util.UUID;

public final class UuidUtils {

    private UuidUtils() {}

    public static String generateUuidWithoutDash() {
        return UUID.randomUUID().toString().replaceAll(CommonConstants.DASH, org.apache.commons.lang3.StringUtils.EMPTY);
    }
}
