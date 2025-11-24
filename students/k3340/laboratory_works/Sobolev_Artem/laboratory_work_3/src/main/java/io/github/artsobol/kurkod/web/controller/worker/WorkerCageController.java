package io.github.artsobol.kurkod.web.controller.worker;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.cage.model.dto.CageDTO;
import io.github.artsobol.kurkod.web.domain.worker.model.dto.WorkerDTO;
import io.github.artsobol.kurkod.web.domain.worker.service.api.WorkerCageService;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@Slf4j
@RestController
@RequestMapping(value = "/api/v1/workers", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Tag(name = "Worker Cages", description = "Assign or remove cages for workers")
public class WorkerCageController {

    private final WorkerCageService workerCageService;

    @Operation(summary = "Get cages assigned to worker", description = "Returns all cages serviced by a worker.")
    @GetMapping("/{workerId}/cages")
    public ResponseEntity<IamResponse<List<CageDTO>>> getWorkerCages(
            @Parameter(description = "Worker identifier", example = "42") @PathVariable Long workerId) {

        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        List<CageDTO> cages = workerCageService.getWorkerCages(workerId);
        return ResponseEntity.ok(IamResponse.createSuccessful(cages));
    }

    @Operation(summary = "Get workers assigned to cage",
               description = "Returns all workers who service the specified cage.")
    @GetMapping("/cages/{cageId}/workers")
    public ResponseEntity<IamResponse<List<WorkerDTO>>> getCageWorkers(
            @Parameter(description = "Cage identifier", example = "12") @PathVariable Long cageId) {

        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        List<WorkerDTO> workers = workerCageService.getCageWorkers(cageId);
        return ResponseEntity.ok(IamResponse.createSuccessful(workers));
    }

    @Operation(summary = "Assign cage to worker", description = "Assigns the specified cage to the worker.")
    @PostMapping("/{workerId}/cages/{cageId}")
    public ResponseEntity<IamResponse<Void>> assignCage(
            @Parameter(description = "Worker identifier", example = "42") @PathVariable Long workerId,
            @Parameter(description = "Cage identifier", example = "10") @PathVariable Long cageId) {

        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        workerCageService.assignCageToWorker(workerId, cageId);
        return ResponseEntity.status(HttpStatus.CREATED).body(IamResponse.createSuccessful(null));
    }

    @Operation(summary = "Unassign cage from worker", description = "Removes the cage assignment from the worker.")
    @DeleteMapping("/{workerId}/cages/{cageId}")
    public ResponseEntity<Void> unassignCage(
            @Parameter(description = "Worker identifier", example = "42") @PathVariable Long workerId,
            @Parameter(description = "Cage identifier", example = "10") @PathVariable Long cageId) {

        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        workerCageService.unassignCageFromWorker(workerId, cageId);
        return ResponseEntity.noContent().build();
    }
}