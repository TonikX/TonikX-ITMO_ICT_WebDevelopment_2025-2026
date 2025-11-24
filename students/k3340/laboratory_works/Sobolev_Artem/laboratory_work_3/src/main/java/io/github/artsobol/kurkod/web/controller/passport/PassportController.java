package io.github.artsobol.kurkod.web.controller.passport;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.EtagUtils;
import io.github.artsobol.kurkod.common.util.LocationUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.passport.model.dto.PassportDTO;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPatchRequest;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPostRequest;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPutRequest;
import io.github.artsobol.kurkod.web.domain.passport.service.api.PassportService;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.enums.ParameterIn;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping(value = "/api/v1/workers/{workerId}/passport", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "Passport", description = "Passport operations")
public class PassportController {

    private final PassportService passportService;

    @Operation(summary = "Get passport by worker ID",
               description = "Returns the passport information for a specific worker.")
    @GetMapping
    public ResponseEntity<IamResponse<PassportDTO>> get(
            @Parameter(description = "Worker identifier", example = "5") @PathVariable(name = "workerId") Long id) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        PassportDTO response = passportService.get(id);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Create a passport for a worker",
               description = "Creates a new passport for the specified worker. Each worker can have only one passport.")
    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<PassportDTO>> create(
            @Parameter(description = "Worker identifier", example = "5") @PathVariable(name = "workerId") Long id,
            @RequestBody @Valid PassportPostRequest request) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        PassportDTO response = passportService.create(id, request);
        return ResponseEntity.created(LocationUtils.buildLocation()).body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Replace a worker’s passport",
               description = "Fully replaces the passport data for the specified worker.")
    @PutMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<PassportDTO>> replace(
            @Parameter(description = "Worker identifier", example = "5") @PathVariable(name = "workerId") Long id,
            @RequestBody @Valid PassportPutRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        PassportDTO response = passportService.replace(id, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Partially update a worker’s passport",
               description = "Applies a partial update to the passport data for the specified worker.")
    @PatchMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<PassportDTO>> update(
            @Parameter(description = "Worker identifier", example = "5") @PathVariable(name = "workerId") Long id,
            @RequestBody @Valid PassportPatchRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        PassportDTO response = passportService.update(id, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Delete a worker’s passport",
               description = "Deletes the passport associated with the specified worker.")
    @DeleteMapping
    public ResponseEntity<Void> delete(
            @Parameter(description = "Worker identifier", example = "5") @PathVariable(name = "workerId") Long id,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        passportService.delete(id, expected);
        return ResponseEntity.noContent().build();
    }
}
