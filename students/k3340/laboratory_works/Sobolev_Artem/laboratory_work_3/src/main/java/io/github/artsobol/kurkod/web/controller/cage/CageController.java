package io.github.artsobol.kurkod.web.controller.cage;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.EtagUtils;
import io.github.artsobol.kurkod.common.util.LocationUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.cage.model.dto.CageDTO;
import io.github.artsobol.kurkod.web.domain.cage.model.request.CagePatchRequest;
import io.github.artsobol.kurkod.web.domain.cage.model.request.CagePostRequest;
import io.github.artsobol.kurkod.web.domain.cage.model.request.CagePutRequest;
import io.github.artsobol.kurkod.web.domain.cage.service.api.CageService;
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
@Tag(name = "Cage", description = "Cage operations")
@RequiredArgsConstructor
@RequestMapping("/api/v1/rows/{rowId}/cage")
public class CageController {

    private final CageService cageService;

    @GetMapping("/{cageNumber}")
    @Operation(summary = "Get cage by cage number", description = "Returns a single cage by its unique number.")
    public ResponseEntity<IamResponse<CageDTO>> get(
            @Parameter(description = "Row identifier", example = "1") @PathVariable(name = "rowId") Long rowId,
            @Parameter(description = "Cage number", example = "2") @PathVariable(name = "cageNumber")
            Integer cageNumber) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        CageDTO response = cageService.find(rowId, cageNumber);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @GetMapping
    @Operation(summary = "Get all cages", description = "Returns all cages available in the system.")
    public ResponseEntity<IamResponse<List<CageDTO>>> getAll(
            @Parameter(description = "Row identifier", example = "1") @PathVariable(name = "rowId") Long rowId) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<CageDTO> response = cageService.findAll(rowId);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @PostMapping
    @Operation(summary = "Create a new cage", description = "Creates a new cage in the system.")
    public ResponseEntity<IamResponse<CageDTO>> create(
            @Parameter(description = "Row identifier", example = "1") @PathVariable(name = "rowId") Long rowId,
            @RequestBody @Valid CagePostRequest cagePostRequest) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        CageDTO response = cageService.create(rowId, cagePostRequest);
        return ResponseEntity.created(LocationUtils.buildLocation(response.cageNumber()))
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @PutMapping("/{cageNumber}")
    @Operation(summary = "Replace cage by cage number", description = "Replaces an existing cage with new data.")
    public ResponseEntity<IamResponse<CageDTO>> replace(
            @Parameter(description = "Row identifier", example = "1") @PathVariable(name = "rowId") Long rowId,
            @Parameter(description = "Cage number", example = "2") @PathVariable(name = "cageNumber")
            Integer cageNumber,
            @RequestBody @Valid CagePutRequest cagePutRequest,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        CageDTO response = cageService.replace(rowId, cageNumber, cagePutRequest, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @PatchMapping("/{cageNumber}")
    @Operation(summary = "Update cage by cage number", description = "Update an existing cage with new data.")
    public ResponseEntity<IamResponse<CageDTO>> update(
            @Parameter(description = "Row identifier", example = "1") @PathVariable(name = "rowId") Long rowId,
            @Parameter(description = "Cage number", example = "2") @PathVariable(name = "cageNumber")
            Integer cageNumber,
            @RequestBody @Valid CagePatchRequest cagePatchRequest,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        CageDTO response = cageService.update(rowId, cageNumber, cagePatchRequest, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @DeleteMapping("/{cageNumber}")
    @Operation(summary = "Delete cage by cage number", description = "Deletes a cage by its unique number.")
    public ResponseEntity<Void> delete(
            @Parameter(description = "Row identifier", example = "1") @PathVariable(name = "rowId") Long rowId,
            @Parameter(description = "Cage number", example = "2") @PathVariable(name = "cageNumber")
            Integer cageNumber,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        cageService.delete(rowId, cageNumber, expected);
        return ResponseEntity.noContent().build();
    }
}
