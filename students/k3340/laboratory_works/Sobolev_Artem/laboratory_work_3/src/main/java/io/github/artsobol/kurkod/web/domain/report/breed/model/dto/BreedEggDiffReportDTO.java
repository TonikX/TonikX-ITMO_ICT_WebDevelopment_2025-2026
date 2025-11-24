package io.github.artsobol.kurkod.web.domain.report.breed.model.dto;

import java.math.BigDecimal;

public record BreedEggDiffReportDTO(
        Long breedId,
        String breedName,
        BigDecimal breedAvgEggs,
        BigDecimal farmAvgEggs,
        BigDecimal diffEggs
) {}