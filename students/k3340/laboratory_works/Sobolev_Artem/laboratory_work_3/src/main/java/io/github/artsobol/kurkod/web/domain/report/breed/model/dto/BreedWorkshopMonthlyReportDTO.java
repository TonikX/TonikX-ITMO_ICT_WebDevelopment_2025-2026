package io.github.artsobol.kurkod.web.domain.report.breed.model.dto;

import java.math.BigDecimal;

public record BreedWorkshopMonthlyReportDTO(
        Long workshopId,
        Integer workshopNumber,
        Long breedId,
        String breedName,
        Long chickensCount,
        Long eggsTotal,
        BigDecimal avgEggsPerChicken
) {}
