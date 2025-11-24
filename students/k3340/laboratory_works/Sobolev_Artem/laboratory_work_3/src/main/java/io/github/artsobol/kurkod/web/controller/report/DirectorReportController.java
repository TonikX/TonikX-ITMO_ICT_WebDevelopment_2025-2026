package io.github.artsobol.kurkod.web.controller.report;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.report.farm.dto.FarmMonthlyReportDTO;
import io.github.artsobol.kurkod.web.domain.report.service.api.FarmReportService;
import io.github.artsobol.kurkod.web.domain.report.breed.model.dto.BreedEggDiffReportDTO;
import io.github.artsobol.kurkod.web.domain.report.breed.serivce.api.BreedReportService;
import io.github.artsobol.kurkod.web.domain.report.chicken.model.dto.ChickenEggStatsDTO;
import io.github.artsobol.kurkod.web.domain.report.chicken.model.dto.ChickensByWorkshopAndBreedDTO;
import io.github.artsobol.kurkod.web.domain.report.chicken.model.dto.WorkshopBreedTopDTO;
import io.github.artsobol.kurkod.web.domain.report.chicken.service.api.ChickenReportService;
import io.github.artsobol.kurkod.web.domain.report.worker.model.dto.WorkerReportDailyEggsDTO;
import io.github.artsobol.kurkod.web.domain.report.worker.service.api.WorkerReportService;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.List;

@Slf4j
@RestController
@RequestMapping(value = "/api/v1/reports/director", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Tag(name = "Director Reports", description = "Director-level analytical reports")
public class DirectorReportController {

    private final FarmReportService farmReportService;
    private final BreedReportService breedReportService;
    private final ChickenReportService chickenReportService;
    private final WorkerReportService workerReportService;

    @Operation(
            summary = "Factory monthly report",
            description = "Returns aggregated monthly metrics for the entire factory."
    )
    @GetMapping("/factory/monthly")
    public ResponseEntity<IamResponse<FarmMonthlyReportDTO>> getFactoryMonthly(
            @Parameter(description = "Target year", example = "2025") @RequestParam int year,
            @Parameter(description = "Target month (1–12)", example = "3") @RequestParam int month
                                                                              ) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        FarmMonthlyReportDTO response = farmReportService.getMonthlyReport(year, month);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(
            summary = "Breed egg difference report",
            description = "Shows difference between each breed’s metrics and factory averages."
    )
    @GetMapping("/breeds/egg-diff")
    public ResponseEntity<IamResponse<List<BreedEggDiffReportDTO>>> getBreedEggDiff() {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<BreedEggDiffReportDTO> response = breedReportService.getEggDiff();
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(
            summary = "Chickens distribution by workshop and breed",
            description = "Returns how many chickens of each breed are located in each workshop."
    )
    @GetMapping("/chickens/by-workshop-and-breed")
    public ResponseEntity<IamResponse<List<ChickensByWorkshopAndBreedDTO>>> getChickensByWorkshopAndBreed() {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<ChickensByWorkshopAndBreedDTO> response = chickenReportService.getChickensByWorkshopAndBreed();
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(
            summary = "Top workshop for a specific breed",
            description = "Returns the workshop with the highest number of chickens of the specified breed."
    )
    @GetMapping("/chickens/top-workshop-by-breed")
    public ResponseEntity<IamResponse<WorkshopBreedTopDTO>> getTopWorkshopByBreed(
            @Parameter(description = "Breed identifier", example = "7") @RequestParam Long breedId
                                                                                 ) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        WorkshopBreedTopDTO response = chickenReportService.getTopWorkshopByBreed(breedId);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(
            summary = "Egg statistics with filters",
            description = "Returns egg statistics for each chicken, filtered by weight, breed or birth date."
    )
    @GetMapping("/chickens/egg-stats")
    public ResponseEntity<IamResponse<List<ChickenEggStatsDTO>>> getChickenEggStats(
            @Parameter(description = "Chicken weight filter", example = "200") @RequestParam(required = false) Integer weight,
            @Parameter(description = "Breed ID filter", example = "5") @RequestParam(required = false) Long breedId,
            @Parameter(description = "Birth date filter", example = "2024-01-15") @RequestParam(required = false) LocalDate birthDate
                                                                                   ) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<ChickenEggStatsDTO> response = chickenReportService.getEggStats(weight, breedId, birthDate);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }

    @Operation(
            summary = "Daily average eggs per worker for a month",
            description = "Returns how many eggs per day each worker collects on average for the given month."
    )
    @GetMapping("/workers/daily-avg-eggs")
    public ResponseEntity<IamResponse<List<WorkerReportDailyEggsDTO>>> getWorkerDailyEggs(
            @Parameter(description = "Target year", example = "2025") @RequestParam int year,
            @Parameter(description = "Target month (1–12)", example = "4") @RequestParam int month
                                                                                         ) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<WorkerReportDailyEggsDTO> response = workerReportService.getWorkerDailyEggs(year, month);
        return ResponseEntity.ok(IamResponse.createSuccessful(response));
    }
}
