package io.github.artsobol.kurkod.web.domain.report.farm.dto;

import io.github.artsobol.kurkod.web.domain.report.breed.model.dto.BreedWorkshopMonthlyReportDTO;

import java.util.List;

public record FarmMonthlyReportDTO(
        int year,
        int month,
        List<BreedWorkshopMonthlyReportDTO> stats,
        long totalChickens,
        long totalEggs
) {}