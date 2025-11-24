package io.github.artsobol.kurkod.web.controller.staff;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.EtagUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.staff.model.dto.StaffDTO;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPatchRequest;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPostRequest;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPutRequest;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.github.artsobol.kurkod.web.domain.staff.service.api.StaffService;
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

import java.net.URI;
import java.util.List;

import static io.github.artsobol.kurkod.web.controller.breed.BreedController.buildLocationUri;

@Slf4j
@RestController
@RequestMapping(value = "/api/v1/staff", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Tag(name = "Staff", description = "Staff operations")
public class StaffController {

    private final StaffService staffService;

    @Operation(summary = "Get staff by ID", description = "Returns a single staff member by their unique identifier.")
    @GetMapping("/{id}")
    public ResponseEntity<IamResponse<StaffDTO>> get(
            @Parameter(description = "Staff identifier", example = "7") @PathVariable Long id) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        StaffDTO response = staffService.get(id);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "List all staff", description = "Returns all staff positions available in the system.")
    @GetMapping
    public ResponseEntity<IamResponse<List<StaffDTO>>> getAll() {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<StaffDTO> response = staffService.getAll();
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Create a new staff position",
               description = "Creates a new staff position. Name must be unique.")
    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<StaffDTO>> create(@Valid @RequestBody StaffPostRequest staffPostRequest) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        StaffDTO response = staffService.create(staffPostRequest);
        URI location = buildLocationUri(response.id());
        return ResponseEntity.created(location)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Replace a staff position", description = "Fully replaces an existing staff position by ID.")
    @PutMapping(value = "/{id}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<StaffDTO>> replace(
            @Parameter(description = "Staff identifier", example = "7") @PathVariable Long id,
            @Valid @RequestBody StaffPutRequest staffPutRequest,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        StaffDTO response = staffService.replace(id, staffPutRequest, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Partially update a staff position",
               description = "Applies a partial update to a staff position by ID.")
    @PatchMapping(value = "/{id}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<StaffDTO>> update(
            @Parameter(description = "Staff identifier", example = "7") @PathVariable Long id,
            @Valid @RequestBody StaffPatchRequest staffPatchRequest,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        StaffDTO response = staffService.update(id, staffPatchRequest, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Delete a staff position", description = "Deletes a staff position by its unique identifier.")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @Parameter(description = "Staff identifier", example = "7") @PathVariable Long id,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        staffService.delete(id, expected);
        return ResponseEntity.noContent().build();
    }
}