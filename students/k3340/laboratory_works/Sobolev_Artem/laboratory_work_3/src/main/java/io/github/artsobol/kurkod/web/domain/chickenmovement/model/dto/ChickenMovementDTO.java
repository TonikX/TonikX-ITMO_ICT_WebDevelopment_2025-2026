package io.github.artsobol.kurkod.web.domain.chickenmovement.model.dto;

import java.time.OffsetDateTime;

public record ChickenMovementDTO(
        Long id, Long chickenId, Long fromCageId, Long toCageId, OffsetDateTime movedAt
) {
};
