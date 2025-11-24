package io.github.artsobol.kurkod.web.domain.common.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum CommonError implements ErrorDescriptor {
    VALIDATION_FAILED("COM-400-VALIDATION", "common.validation_failed", HttpStatus.BAD_REQUEST),
    MALFORMED_JSON("COM-400-JSON",
                   "common.malformed_json",
                   HttpStatus.BAD_REQUEST),
    UNSUPPORTED_MEDIA_TYPE("COM-415",
                           "common.unsupported_media",
                           HttpStatus.UNSUPPORTED_MEDIA_TYPE),
    METHOD_NOT_ALLOWED("COM-405",
                       "common.method_not_allowed",
                       HttpStatus.METHOD_NOT_ALLOWED),
    NOT_ACCEPTABLE("COM-406",
                   "common.not_acceptable",
                   HttpStatus.NOT_ACCEPTABLE),
    MISSING_IF_MATCH("COM-428",
                     "common.ifmatch_missing",
                     HttpStatus.PRECONDITION_REQUIRED),
    INVALID_IF_MATCH("COM-400-IFM", "common.ifmatch_invalid", HttpStatus.BAD_REQUEST),
    PRECONDITION_FAILED("COM-412", "common.precondition_failed", HttpStatus.PRECONDITION_FAILED),
    INTERNAL_ERROR("COM-500", "common.internal_error", HttpStatus.INTERNAL_SERVER_ERROR),
    BAD_REQUEST("COM-400", "common.bad_request", HttpStatus.BAD_REQUEST),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;
}
