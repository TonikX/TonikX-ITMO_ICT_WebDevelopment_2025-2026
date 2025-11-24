package io.github.artsobol.kurkod.web.domain.worker.repository;

import io.github.artsobol.kurkod.web.domain.worker.model.entity.WorkerCage;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface WorkerCageRepository extends JpaRepository<WorkerCage, Long> {

    List<WorkerCage> findAllByWorkerId(Long workerId);

    List<WorkerCage> findAllByCageId(Long cageId);

    boolean existsByWorkerIdAndCageId(Long workerId, Long cageId);

    boolean existsByWorkerId(Long workerId);

    boolean existsByCageId(Long cageId);

    void deleteByWorkerIdAndCageId(Long workerId, Long cageId);

    void deleteAllByWorkerId(Long workerId);

    void deleteAllByCageId(Long cageId);

    long countByWorkerId(Long workerId);

    long countByCageId(Long cageId);
}

