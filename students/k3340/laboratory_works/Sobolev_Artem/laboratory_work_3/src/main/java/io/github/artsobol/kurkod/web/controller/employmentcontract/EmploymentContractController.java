package io.github.artsobol.kurkod.web.controller.employmentcontract;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.EtagUtils;
import io.github.artsobol.kurkod.common.util.LocationUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.dto.EmploymentContractDTO;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.request.EmploymentContractPatchRequest;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.request.EmploymentContractPostRequest;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.request.EmploymentContractPutRequest;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.github.artsobol.kurkod.web.domain.employmentcontract.service.api.EmploymentContractService;
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
@RequestMapping(value = "/api/v1/workers/{workerId}/contract", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "Employment Contract", description = "Employment Contract operations")
public class EmploymentContractController {

    private final EmploymentContractService employmentContractService;

    @Operation(summary = "Get employment contract by worker ID",
               description = "Returns the employment contract information for the specified worker.")
    @GetMapping
    public ResponseEntity<IamResponse<EmploymentContractDTO>> get(
            @Parameter(description = "Worker identifier", example = "12") @PathVariable(name = "workerId")
            Long workerId) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        EmploymentContractDTO response = employmentContractService.get(workerId);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Create an employment contract for a worker",
               description = "Creates a new employment contract for the specified worker. Each worker can have only one active contract.")
    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<EmploymentContractDTO>> create(
            @PathVariable(name = "workerId") Long workerId,
            @RequestBody @Valid EmploymentContractPostRequest request) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        EmploymentContractDTO response = employmentContractService.create(workerId, request);
        return ResponseEntity.created(LocationUtils.buildLocation()).eTag(EtagUtils.toEtag(response.version())).body(
                IamResponse.createSuccessful(response));
    }


    @Operation(summary = "Replace an employment contract",
               description = "Fully replaces the employment contract data for the specified worker.")
    @PutMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<EmploymentContractDTO>> replace(
            @Parameter(description = "Worker identifier", example = "12") @PathVariable(name = "workerId")
            Long workerId,
            @RequestBody @Valid EmploymentContractPutRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        EmploymentContractDTO response = employmentContractService.replace(workerId, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Partially update an employment contract",
               description = "Applies a partial update to the employment contract for the specified worker.")
    @PatchMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<EmploymentContractDTO>> update(
            @Parameter(description = "Worker identifier", example = "12") @PathVariable(name = "workerId")
            Long workerId,
            @RequestBody @Valid EmploymentContractPatchRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        EmploymentContractDTO response = employmentContractService.update(workerId, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Delete an employment contract",
               description = "Deletes the employment contract associated with the specified worker.")
    @DeleteMapping
    public ResponseEntity<Void> delete(
            @Parameter(description = "Worker identifier", example = "12") @PathVariable(name = "workerId")
            Long workerId,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        employmentContractService.delete(workerId, expected);
        return ResponseEntity.noContent().build();
    }
}
