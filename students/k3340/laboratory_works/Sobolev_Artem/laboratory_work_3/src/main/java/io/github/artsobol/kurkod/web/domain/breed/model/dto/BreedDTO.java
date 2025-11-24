package io.github.artsobol.kurkod.web.domain.breed.model.dto;

public record BreedDTO(
        Long id, String name, Integer eggsNumber, Integer weight, Long version
) {};
