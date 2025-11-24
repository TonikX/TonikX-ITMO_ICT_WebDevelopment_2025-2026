package io.github.artsobol.kurkod.web.controller.eggproductionmonth;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.EtagUtils;
import io.github.artsobol.kurkod.common.util.LocationUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.dto.EggProductionMonthDTO;
import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.request.EggProductionMonthPatchRequest;
import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.request.EggProductionMonthPostRequest;
import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.request.EggProductionMonthPutRequest;
import io.github.artsobol.kurkod.web.domain.eggproductionmonth.service.api.EggProductionMonthService;
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
@RequiredArgsConstructor
@Tag(name = "Egg Production Month", description = "Egg Production Month operations")
@RequestMapping("/api/v1/chickens/{chickenId}/egg-productions")
public class EggProductionMonthController {

    private final EggProductionMonthService eggProductionMonthService;

    @PostMapping("/{year}/{month}")
    @Operation(summary = "Create egg production month",
               description = "Creates a new egg production month for the specified chicken.")
    public ResponseEntity<IamResponse<EggProductionMonthDTO>> create(
            @Parameter(description = "Chicken identifier", example = "1") @PathVariable(name = "chickenId")
            Long chickenId,
            @Parameter(description = "Year", example = "2020") @PathVariable(name = "year") Integer year,
            @Parameter(description = "Month", example = "5") @PathVariable(name = "month") Integer month,
            @Valid @RequestBody EggProductionMonthPostRequest request) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        EggProductionMonthDTO response = eggProductionMonthService.create(chickenId, month, year, request);
        return ResponseEntity.created(LocationUtils.buildLocation()).eTag(EtagUtils.toEtag(response.version())).body(
                IamResponse.createSuccessful(response));
    }

    @GetMapping("/{year}/{month}")
    @Operation(summary = "Get egg production month by chicken ID, year and month",
               description = "Returns an egg production month by its unique identifier.")
    public ResponseEntity<IamResponse<EggProductionMonthDTO>> getById(
            @Parameter(description = "Chicken identifier", example = "1") @PathVariable(name = "chickenId")
            Long chickenId,
            @Parameter(description = "Year", example = "2020") @PathVariable(name = "year") Integer year,
            @Parameter(description = "Month", example = "5") @PathVariable(name = "month") Integer month) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        EggProductionMonthDTO response = eggProductionMonthService.get(chickenId, month, year);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @GetMapping
    @Operation(summary = "Get all egg production months", description = "Returns all egg production months.")
    public ResponseEntity<IamResponse<List<EggProductionMonthDTO>>> getAllByChickenId(
            @Parameter(description = "Chicken identifier", example = "1") @PathVariable(name = "chickenId")
            Long chickenId) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        List<EggProductionMonthDTO> response = eggProductionMonthService.getAllByChicken(chickenId);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @GetMapping("/{year}")
    @Operation(summary = "Get all egg production months for year",
               description = "Returns all egg production months for year")
    public ResponseEntity<IamResponse<List<EggProductionMonthDTO>>> getAllByChickenIdAndYear(
            @Parameter(description = "Chicken identifier", example = "1") @PathVariable(name = "chickenId")
            Long chickenId,
            @Parameter(description = "Year", example = "2020") @PathVariable(name = "year") Integer year) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        List<EggProductionMonthDTO> response = eggProductionMonthService.getAllByChickenAndYear(chickenId, year);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @PutMapping("/{year}/{month}")
    @Operation(summary = "Replace egg production month", description = "Fully replaces an egg production month by ID.")
    public ResponseEntity<IamResponse<EggProductionMonthDTO>> replace(
            @Parameter(description = "Chicken identifier", example = "1") @PathVariable(name = "chickenId")
            Long chickenId,
            @Parameter(description = "Year", example = "2020") @PathVariable(name = "year") Integer year,
            @Parameter(description = "Month", example = "5") @PathVariable(name = "month") Integer month,
            @Valid @RequestBody EggProductionMonthPutRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        EggProductionMonthDTO response = eggProductionMonthService.replace(chickenId, month, year, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @PatchMapping("/{year}/{month}")
    @Operation(summary = "Update egg production month",
               description = "Update an existing egg production month with new data.")
    public ResponseEntity<IamResponse<EggProductionMonthDTO>> update(
            @Parameter(description = "Chicken identifier", example = "1") @PathVariable(name = "chickenId")
            Long chickenId,
            @Parameter(description = "Year", example = "2020") @PathVariable(name = "year") Integer year,
            @Parameter(description = "Month", example = "5") @PathVariable(name = "month") Integer month,
            @Valid @RequestBody EggProductionMonthPatchRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        EggProductionMonthDTO response = eggProductionMonthService.update(chickenId, month, year, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @DeleteMapping("/{year}/{month}")
    @Operation(summary = "Delete egg production month",
               description = "Deletes an existing egg production month by its unique identifier.")
    public ResponseEntity<Void> delete(
            @Parameter(description = "Chicken identifier", example = "1") @PathVariable(name = "chickenId")
            Long chickenId,
            @Parameter(description = "Year", example = "2020") @PathVariable(name = "year") Integer year,
            @Parameter(description = "Month", example = "5") @PathVariable(name = "month") Integer month,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        eggProductionMonthService.delete(chickenId, month, year, expected);
        return ResponseEntity.noContent().build();
    }

}
