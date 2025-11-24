package io.github.artsobol.kurkod.web.domain.diet.model.dto;

import io.github.artsobol.kurkod.web.domain.common.model.Season;

public record DietDTO(
        Integer id, String title, String code, String description, Season season, Long version
) {
};
