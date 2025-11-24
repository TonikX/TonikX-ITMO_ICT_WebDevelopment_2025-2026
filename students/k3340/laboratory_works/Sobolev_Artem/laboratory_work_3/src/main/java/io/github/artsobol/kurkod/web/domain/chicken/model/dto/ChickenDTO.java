package io.github.artsobol.kurkod.web.domain.chicken.model.dto;


import java.time.LocalDate;

public record ChickenDTO(
        Long id,
        String name,
        Integer weight,
        LocalDate birthDate,
        Long breedId,
        Long cageId,
        Long version
) {
};
