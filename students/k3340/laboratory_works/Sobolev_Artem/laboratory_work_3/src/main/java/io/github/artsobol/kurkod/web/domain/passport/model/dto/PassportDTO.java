package io.github.artsobol.kurkod.web.domain.passport.model.dto;


import java.time.OffsetDateTime;

public record PassportDTO(
        String series, String number, OffsetDateTime createdAt, OffsetDateTime updatedAt, Long version
) {
};