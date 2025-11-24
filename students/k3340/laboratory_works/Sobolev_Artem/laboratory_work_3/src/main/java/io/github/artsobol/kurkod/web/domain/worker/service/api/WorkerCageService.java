package io.github.artsobol.kurkod.web.domain.worker.service.api;

import io.github.artsobol.kurkod.web.domain.cage.model.dto.CageDTO;
import io.github.artsobol.kurkod.web.domain.worker.model.dto.WorkerDTO;

import java.util.List;

public interface WorkerCageService {

    List<CageDTO> getWorkerCages(Long workerId);

    List<WorkerDTO> getCageWorkers(Long cageId);

    void assignCageToWorker(Long workerId, Long cageId);

    void unassignCageFromWorker(Long workerId, Long cageId);

    boolean hasWorkerAnyCages(Long workerId);

    boolean isCageServedByAnyWorker(Long cageId);
}
