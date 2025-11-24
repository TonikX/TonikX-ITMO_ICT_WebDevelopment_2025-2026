package io.github.artsobol.kurkod.web.domain.report.worker.repository;

import io.github.artsobol.kurkod.web.domain.worker.model.entity.Worker;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface WorkerReportRepository extends JpaRepository<Worker, Long> {

    @Query(value = """
        SELECT
            w.id          AS workerId,
            w.first_name  AS firstName,
            w.last_name   AS lastName,
            COALESCE(SUM(epm.count), 0) AS eggsPerMonth
        FROM worker w
        LEFT JOIN worker_cage wc
            ON wc.worker_id = w.id
        LEFT JOIN cage c
            ON c.id = wc.cage_id
        LEFT JOIN chicken ch
            ON ch.cage_id = c.id
        LEFT JOIN egg_production_month epm
            ON epm.chicken_id = ch.id
           AND epm.year = :year
           AND epm.month = :month
        GROUP BY w.id, w.first_name, w.last_name
        ORDER BY w.last_name, w.first_name
        """,
           nativeQuery = true)
    List<WorkerMonthlyEggsProjection> getMonthlyEggsPerWorker(@Param("year") int year,
                                                          @Param("month") int month);
}
