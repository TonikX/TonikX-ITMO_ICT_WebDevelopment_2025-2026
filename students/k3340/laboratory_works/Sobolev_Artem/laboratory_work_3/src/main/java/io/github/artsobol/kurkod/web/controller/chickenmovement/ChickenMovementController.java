package io.github.artsobol.kurkod.web.controller.chickenmovement;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.LocationUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.chickenmovement.model.dto.ChickenMovementDTO;
import io.github.artsobol.kurkod.web.domain.chickenmovement.model.request.ChickenMovementPostRequest;
import io.github.artsobol.kurkod.web.domain.chickenmovement.service.api.ChickenMovementService;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping(value = "/api/v1", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "Chicken Movement", description = "Operations with chicken movements (history of relocations)")
public class ChickenMovementController {

    private final ChickenMovementService chickenMovementService;

    @Operation(summary = "Get movement by ID", description = "Returns a single movement by its unique identifier.")
    @GetMapping("/chicken-movements/{id}")
    public ResponseEntity<IamResponse<ChickenMovementDTO>> getById(
            @Parameter(description = "Movement identifier", example = "15") @PathVariable Long id) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        ChickenMovementDTO response = chickenMovementService.get(id);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "List movements by chicken",
               description = "Returns all movements for a chicken, newest first.")
    @GetMapping("/chickens/{chickenId}/movements")
    public ResponseEntity<IamResponse<List<ChickenMovementDTO>>> getAllByChicken(
            @Parameter(description = "Chicken identifier", example = "7") @PathVariable Long chickenId) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<ChickenMovementDTO> response = chickenMovementService.getAllByChickenId(chickenId);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Get current movement for chicken",
               description = "Returns the last movement for a chicken (current location derived from 'toCageId').")
    @GetMapping("/chickens/{chickenId}/movements/current")
    public ResponseEntity<IamResponse<ChickenMovementDTO>> getCurrent(
            @Parameter(description = "Chicken identifier", example = "7") @PathVariable Long chickenId) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        ChickenMovementDTO response = chickenMovementService.getCurrentCage(chickenId);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Create a new movement for chicken", description = """
                                                                            Creates a new movement (relocation) record for the specified chicken.
                                                                            If 'fromCageId' is omitted, the current cage of the chicken is used (may be null for the very first placement).
                                                                            'toCageId' is required.
                                                                            """)
    @PostMapping(value = "/chickens/{chickenId}/movements", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<ChickenMovementDTO>> create(
            @Parameter(description = "Chicken identifier", example = "7") @PathVariable Long chickenId,
            @Valid @RequestBody ChickenMovementPostRequest request) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        ChickenMovementDTO response = chickenMovementService.create(chickenId, request);
        return ResponseEntity.created(LocationUtils.buildLocation()).body(IamResponse.createSuccessful(response));
    }
}