package io.github.artsobol.kurkod.web.controller.worker;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.EtagUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.worker.model.dto.WorkerDTO;
import io.github.artsobol.kurkod.web.domain.worker.model.request.WorkerPatchRequest;
import io.github.artsobol.kurkod.web.domain.worker.model.request.WorkerPostRequest;
import io.github.artsobol.kurkod.web.domain.worker.model.request.WorkerPutRequest;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.github.artsobol.kurkod.web.domain.worker.service.api.WorkerService;
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

import java.util.List;

import static io.github.artsobol.kurkod.common.util.LocationUtils.buildLocation;

@Slf4j
@RestController
@RequestMapping(value = "/api/v1/workers", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Tag(name = "Workers", description = "Worker operations")
public class WorkerController {

    private final WorkerService workerService;

    @Operation(summary = "Get worker by ID", description = "Returns a single worker by its unique identifier.")
    @GetMapping("/{id}")
    public ResponseEntity<IamResponse<WorkerDTO>> get(
            @Parameter(description = "Worker identifier", example = "42") @PathVariable(name = "id") Long id) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        WorkerDTO response = workerService.get(id);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "List all workers", description = "Returns all workers.")
    @GetMapping
    public ResponseEntity<IamResponse<List<WorkerDTO>>> getAll() {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<WorkerDTO> response = workerService.getAll();
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Create a worker", description = "Creates a new worker entity.")
    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<WorkerDTO>> create(@RequestBody @Valid WorkerPostRequest request) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        WorkerDTO response = workerService.create(request);
        return ResponseEntity.created(buildLocation(response.id())).eTag(EtagUtils.toEtag(response.version())).body(
                IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Replace a worker", description = "Fully replaces a worker by ID.")
    @PutMapping(value = "/{id}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<WorkerDTO>> replace(
            @Parameter(description = "Worker identifier", example = "42") @PathVariable(name = "id") Long id,
            @RequestBody @Valid WorkerPutRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false) String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        WorkerDTO response = workerService.replace(id, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Partially update a worker", description = "Applies a partial update to a worker by ID.")
    @PatchMapping(value = "/{id}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<WorkerDTO>> update(
            @Parameter(description = "Worker identifier", example = "42") @PathVariable(name = "id") Long id,
            @RequestBody @Valid WorkerPatchRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false) String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        WorkerDTO response = workerService.update(id, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Delete a worker", description = "Deletes a worker by its unique identifier.")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @Parameter(description = "Worker identifier", example = "42") @PathVariable(name = "id") Long id,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false) String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        workerService.delete(id, expected);
        return ResponseEntity.noContent().build();
    }
}
