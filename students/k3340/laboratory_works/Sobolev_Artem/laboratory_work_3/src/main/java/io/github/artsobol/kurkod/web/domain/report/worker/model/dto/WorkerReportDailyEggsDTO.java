package io.github.artsobol.kurkod.web.domain.report.worker.model.dto;

import java.math.BigDecimal;

public record WorkerReportDailyEggsDTO(
        Long workerId,
        String firstName,
        String lastName,
        BigDecimal avgEggsPerDay
){}
