package io.github.artsobol.kurkod.web.domain.report.chicken.model.dto;

public record WorkshopBreedTopDTO(
        Long workshopId,
        Long workshopNumber,
        Long breedId,
        String breedName,
        Long chickensCount
) {}