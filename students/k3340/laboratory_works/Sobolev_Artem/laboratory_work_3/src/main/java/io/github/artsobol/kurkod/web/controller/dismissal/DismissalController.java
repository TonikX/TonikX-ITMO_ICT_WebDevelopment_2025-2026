package io.github.artsobol.kurkod.web.controller.dismissal;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.EtagUtils;
import io.github.artsobol.kurkod.common.util.LocationUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.security.facade.SecurityContextFacade;
import io.github.artsobol.kurkod.web.domain.dismissal.model.dto.DismissalDTO;
import io.github.artsobol.kurkod.web.domain.dismissal.model.request.DismissalPatchRequest;
import io.github.artsobol.kurkod.web.domain.dismissal.model.request.DismissalPostRequest;
import io.github.artsobol.kurkod.web.domain.dismissal.model.request.DismissalPutRequest;
import io.github.artsobol.kurkod.web.domain.dismissal.service.api.DismissalService;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.enums.ParameterIn;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Slf4j
@RestController
@RequestMapping("/api/v1/dismissals")
@RequiredArgsConstructor
@Tag(name = "Dismissals", description = "Dismissals API")
public class DismissalController {

    private final DismissalService dismissalService;
    private final SecurityContextFacade securityContextFacade;

    @GetMapping("/workers/{workerId}/dismissed/{dismissedId}")
    @Operation(summary = "Get dismissal by worker and dismissed",
               description = "Returns a single dismissal by worker and dismissed.")
    public ResponseEntity<IamResponse<DismissalDTO>> getByWorkerAndDismissed(
            @Parameter(name = "worker id", example = "1") @PathVariable(name = "workerId") Long workerId,
            @Parameter(name = "dismissed id", example = "1") @PathVariable(name = "dismissedId") Long dismissedId) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        DismissalDTO response = dismissalService.getByWorkerAndDismissed(workerId, dismissedId);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @GetMapping("/dismissed/{dismissedId}")
    @Operation(summary = "Get dismissals by dismissed", description = "Returns all dismissals by dismissed.")
    public ResponseEntity<IamResponse<List<DismissalDTO>>> getAllByDismissed(
            @Parameter(name = "dismissed id", example = "1") @PathVariable(name = "dismissedId") Long dismissedId) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<DismissalDTO> response = dismissalService.getAllByDismissed(dismissedId);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @GetMapping("/workers/{workerId}")
    @Operation(summary = "Get dismissals by worker", description = "Returns all dismissals by worker.")
    public ResponseEntity<IamResponse<List<DismissalDTO>>> getAllByWorker(
            @Parameter(name = "worker id", example = "1") @PathVariable(name = "workerId") Long workerId) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<DismissalDTO> response = dismissalService.getAllByWorker(workerId);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @PostMapping
    @Operation(summary = "Create a dismissal", description = "Creates a new dismissal.")
    public ResponseEntity<IamResponse<DismissalDTO>> create(
            @RequestBody @Valid DismissalPostRequest request) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        DismissalDTO response = dismissalService.create(request);
        return ResponseEntity.created(LocationUtils.buildLocation(request.getWorkerId(),
                                                                  securityContextFacade.getCurrentUserId())).eTag(
                EtagUtils.toEtag(response.version())).body(IamResponse.createSuccessful(response));
    }

    @PutMapping("/{workerId}")
    @Operation(summary = "Replace dismissal by worker id", description = "Replace an existing dismissal with new data.")
    public ResponseEntity<IamResponse<DismissalDTO>> replace(
            @Parameter(name = "worker id", example = "1") @PathVariable(name = "workerId") Long workerId,
            @RequestBody @Valid DismissalPutRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        DismissalDTO response = dismissalService.replace(workerId, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @PatchMapping("/{workerId}")
    @Operation(summary = "Update dismissal by worker id", description = "Update an existing dismissal with new data.")
    public ResponseEntity<IamResponse<DismissalDTO>> update(
            @Parameter(name = "worker id", example = "1") @PathVariable(name = "workerId") Long workerId,
            @RequestBody @Valid DismissalPatchRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        DismissalDTO response = dismissalService.update(workerId, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

}
