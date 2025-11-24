package io.github.artsobol.kurkod.web.domain.worker.model.dto;

import io.github.artsobol.kurkod.web.domain.cage.model.dto.CageDTO;

import java.util.Set;

public record WorkerDTO(
        Long id, String firstName, String lastName, String patronymic, Set<CageDTO> cages, Long version
) {
}