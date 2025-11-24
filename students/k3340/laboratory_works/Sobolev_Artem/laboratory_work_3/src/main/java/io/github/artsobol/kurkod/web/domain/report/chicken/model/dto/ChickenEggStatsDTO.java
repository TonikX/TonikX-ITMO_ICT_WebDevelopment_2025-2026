package io.github.artsobol.kurkod.web.domain.report.chicken.model.dto;


import java.time.LocalDate;

public record ChickenEggStatsDTO(
        Long chickenId,
        String chickenName,
        Long breedId,
        String breedName,
        Integer weight,
        LocalDate birthDate,
        Long eggsCount
) {}