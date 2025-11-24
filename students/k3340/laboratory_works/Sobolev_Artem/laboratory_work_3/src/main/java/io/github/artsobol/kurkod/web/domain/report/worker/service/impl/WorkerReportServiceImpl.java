package io.github.artsobol.kurkod.web.domain.report.worker.service.impl;

import io.github.artsobol.kurkod.web.domain.report.worker.model.dto.WorkerReportDailyEggsDTO;
import io.github.artsobol.kurkod.web.domain.report.worker.repository.WorkerReportRepository;
import io.github.artsobol.kurkod.web.domain.report.worker.service.api.WorkerReportService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.YearMonth;
import java.util.List;

@Service
@RequiredArgsConstructor
@PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
@Transactional(readOnly = true)
public class WorkerReportServiceImpl implements WorkerReportService {

    private final WorkerReportRepository workerRepository;

    @Override
    public List<WorkerReportDailyEggsDTO> getWorkerDailyEggs(int year, int month) {
        YearMonth ym = YearMonth.of(year, month);
        int daysInMonth = ym.lengthOfMonth();

        return workerRepository.getMonthlyEggsPerWorker(year, month)
                               .stream()
                               .map(p -> new WorkerReportDailyEggsDTO(
                                       p.getWorkerId(),
                                       p.getFirstName(),
                                       p.getLastName(),
                                       BigDecimal.valueOf(p.getEggsPerMonth())
                                                 .divide(BigDecimal.valueOf(daysInMonth), 2, RoundingMode.HALF_UP)
                               ))
                               .toList();
    }
}


