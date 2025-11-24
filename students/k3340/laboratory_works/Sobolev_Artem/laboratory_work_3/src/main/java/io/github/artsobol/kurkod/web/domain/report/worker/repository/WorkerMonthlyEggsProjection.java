package io.github.artsobol.kurkod.web.domain.report.worker.repository;

public interface WorkerMonthlyEggsProjection {
    Long getWorkerId();
    String getFirstName();
    String getLastName();
    Long getEggsPerMonth();
}
