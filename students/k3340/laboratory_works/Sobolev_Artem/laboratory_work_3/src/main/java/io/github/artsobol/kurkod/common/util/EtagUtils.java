package io.github.artsobol.kurkod.common.util;

import io.github.artsobol.kurkod.common.exception.*;
import io.github.artsobol.kurkod.web.domain.common.error.RequiredHeaderError;

public final class EtagUtils {

    private EtagUtils(){

    }

    public static String toEtag(long version){
        return "\"" + version + "\"";
    }

    public static long parseIfMatch(String ifMatchHeader) {
        checkIfMatch(ifMatchHeader);

        try {
            return parseValue(ifMatchHeader.trim());
        } catch (NumberFormatException e) {
            throw new InvalidIfMatchException(RequiredHeaderError.MATCH_INVALID, ifMatchHeader);
        }
    }

    private static void checkIfMatch(String ifMatchHeader) {
        if (ifMatchHeader == null || ifMatchHeader.isBlank()) {
            throw new MissingIfMatchException(RequiredHeaderError.IF_MATCH, ifMatchHeader);
        }
    }

    private static long parseValue(String headerValue) throws NumberFormatException{
        if (headerValue.startsWith("W/")) {
            headerValue = headerValue.substring(2);
        }
        headerValue = headerValue.replace("\"", "");
        return Long.parseLong(headerValue);
    }

    public static boolean matches(String ifMatchHeader, long currentVersion) {
        return ifMatchHeader != null && ifMatchHeader.equals(toEtag(currentVersion));
    }


}
