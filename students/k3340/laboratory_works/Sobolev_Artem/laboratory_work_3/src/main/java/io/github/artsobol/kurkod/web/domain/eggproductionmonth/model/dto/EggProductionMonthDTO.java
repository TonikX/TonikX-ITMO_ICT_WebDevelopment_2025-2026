package io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.dto;

public record EggProductionMonthDTO(
        Integer id, Integer month, Integer year, Integer count, Integer chickenId, Long version
) {
};