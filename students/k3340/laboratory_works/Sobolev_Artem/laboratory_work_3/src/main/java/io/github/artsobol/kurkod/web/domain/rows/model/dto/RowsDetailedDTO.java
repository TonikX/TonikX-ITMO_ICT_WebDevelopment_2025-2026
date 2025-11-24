package io.github.artsobol.kurkod.web.domain.rows.model.dto;

import io.github.artsobol.kurkod.web.domain.cage.model.entity.Cage;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.time.OffsetDateTime;
import java.util.List;

public record RowsDetailedDTO(
        Long id,
        Integer rowNumber,
        Integer workshopNumber,
        List<Cage> cages,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt
) {
};
