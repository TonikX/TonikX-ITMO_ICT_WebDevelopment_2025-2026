package io.github.artsobol.kurkod.web.domain.report.service.api;

import io.github.artsobol.kurkod.web.domain.report.farm.dto.FarmMonthlyReportDTO;

public interface FarmReportService {

    FarmMonthlyReportDTO getMonthlyReport(int year, int month);
}
