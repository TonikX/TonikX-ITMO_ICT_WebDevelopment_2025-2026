package io.github.artsobol.kurkod.web.domain.report.worker.service.api;

import io.github.artsobol.kurkod.web.domain.report.worker.model.dto.WorkerReportDailyEggsDTO;

import java.util.List;

public interface WorkerReportService {

    List<WorkerReportDailyEggsDTO> getWorkerDailyEggs(int year, int month);
}
