package io.github.artsobol.kurkod.web.domain.staff.model.dto;

import java.time.OffsetDateTime;

public record StaffDTO(
        Long id, String position, OffsetDateTime createdAt, OffsetDateTime updatedAt, Long version
) {
};
