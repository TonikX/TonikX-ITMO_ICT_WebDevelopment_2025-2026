package io.github.artsobol.kurkod.web.advice;

import io.github.artsobol.kurkod.common.exception.*;
import io.github.artsobol.kurkod.web.domain.common.error.CommonError;
import io.github.artsobol.kurkod.web.domain.iam.user.error.UserError;
import io.github.artsobol.kurkod.web.response.IamError;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.ConstraintViolationException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.MessageSource;
import org.springframework.context.NoSuchMessageException;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.HttpMediaTypeNotSupportedException;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingRequestHeaderException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.Locale;

@Slf4j
@RequiredArgsConstructor
@RestControllerAdvice
public class CommonControllerAdvice {

    private final MessageSource messageSource;

    @ExceptionHandler(BaseException.class)
    public ResponseEntity<IamError> handleBaseException(BaseException ex, HttpServletRequest request) {
        logBusinessError(ex, request);
        return buildResponse(ex, request);
    }

    @ExceptionHandler(MissingServletRequestParameterException.class)
    public ResponseEntity<IamError> handleMissingParameter(
            HttpServletRequest request) {
        return buildResponse(Exceptions.of(CommonError.BAD_REQUEST), request);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<IamError> handleMethodArgumentNotValid(
            HttpServletRequest request) {
        return buildResponse(Exceptions.of(CommonError.VALIDATION_FAILED), request);
    }

    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<IamError> handleConstraintViolation(
            HttpServletRequest request) {
        return buildResponse(Exceptions.of(CommonError.VALIDATION_FAILED), request);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<IamError> handleUnreadableBody(
            HttpServletRequest request) {
        return buildResponse(Exceptions.of(CommonError.MALFORMED_JSON), request);
    }

    @ExceptionHandler(HttpMediaTypeNotSupportedException.class)
    public ResponseEntity<IamError> handleUnsupportedMediaType(
            HttpServletRequest request) {
        return buildResponse(Exceptions.of(CommonError.UNSUPPORTED_MEDIA_TYPE), request);
    }

    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public ResponseEntity<IamError> handleMethodNotAllowed(
            HttpServletRequest request) {
        return buildResponse(Exceptions.of(CommonError.METHOD_NOT_ALLOWED), request);
    }

    @ExceptionHandler(MissingRequestHeaderException.class)
    public ResponseEntity<IamError> handleMissingHeader(MissingRequestHeaderException ex, HttpServletRequest request) {
        if ("If-Match".equalsIgnoreCase(ex.getHeaderName())) {
            return buildResponse(Exceptions.of(CommonError.MISSING_IF_MATCH), request);
        }
        return buildResponse(Exceptions.of(CommonError.VALIDATION_FAILED), request);
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<IamError> handleAccessDenied(
            HttpServletRequest request) {
        return buildResponse(Exceptions.of(UserError.HAVE_NO_ACCESS), request);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<IamError> handleUnexpected(Exception ex, HttpServletRequest request) {
        log.error("Unexpected error on path={}", request.getRequestURI(), ex);
        return buildResponse(Exceptions.of(CommonError.INTERNAL_ERROR), request);
    }

    private void logBusinessError(BaseException ex, HttpServletRequest request) {
        log.warn("Business error: status={}, code={}, key={}, path={}, args={}",
                 ex.getStatus(),
                 ex.getCode(),
                 ex.getMessageKey(),
                 request.getRequestURI(),
                 Arrays.toString(ex.getArgs()));
    }

    private ResponseEntity<IamError> buildResponse(BaseException ex, HttpServletRequest request) {
        IamError error = createError(ex, request);
        return ResponseEntity.status(error.getStatus()).contentType(MediaType.APPLICATION_JSON).body(error);
    }

    protected IamError createError(BaseException ex, HttpServletRequest request) {
        String message = getLocalizedMessage(ex);
        String path = request.getRequestURI();
        return IamError.createError(ex.getStatus(), ex.getCode(), message, path);
    }

    protected String getLocalizedMessage(BaseException ex) {
        Locale locale = LocaleContextHolder.getLocale();
        try {
            return messageSource.getMessage(ex.getMessageKey(), ex.getArgs(), locale);
        } catch (NoSuchMessageException e) {
            log.warn("No message found for key={} and locale={}", ex.getMessageKey(), locale);
            if (ex.getMessage() != null) {
                return ex.getMessage();
            }
            return ex.getMessageKey();
        }
    }
}

