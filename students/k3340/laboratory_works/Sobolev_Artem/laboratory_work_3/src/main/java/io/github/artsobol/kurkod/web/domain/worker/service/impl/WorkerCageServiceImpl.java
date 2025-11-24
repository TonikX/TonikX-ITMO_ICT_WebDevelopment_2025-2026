package io.github.artsobol.kurkod.web.domain.worker.service.impl;

import io.github.artsobol.kurkod.common.exception.DataExistException;
import io.github.artsobol.kurkod.web.domain.cage.error.CageError;
import io.github.artsobol.kurkod.web.domain.cage.mapper.CageMapper;
import io.github.artsobol.kurkod.web.domain.cage.model.dto.CageDTO;
import io.github.artsobol.kurkod.web.domain.cage.model.entity.Cage;
import io.github.artsobol.kurkod.web.domain.cage.repository.CageRepository;
import io.github.artsobol.kurkod.web.domain.worker.error.WorkerError;
import io.github.artsobol.kurkod.web.domain.worker.mapper.WorkerMapper;
import io.github.artsobol.kurkod.web.domain.worker.model.dto.WorkerDTO;
import io.github.artsobol.kurkod.web.domain.worker.model.entity.Worker;
import io.github.artsobol.kurkod.web.domain.worker.model.entity.WorkerCage;
import io.github.artsobol.kurkod.web.domain.worker.repository.WorkerCageRepository;
import io.github.artsobol.kurkod.web.domain.worker.repository.WorkerRepository;
import io.github.artsobol.kurkod.web.domain.worker.service.api.WorkerCageService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
@PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
@RequiredArgsConstructor
public class WorkerCageServiceImpl implements WorkerCageService {

    private final WorkerRepository workerRepository;
    private final CageRepository cageRepository;
    private final WorkerCageRepository workerCageRepository;
    private final CageMapper cageMapper;
    private final WorkerMapper workerMapper;

    @Override
    @Transactional(readOnly = true)
    public List<CageDTO> getWorkerCages(Long workerId) {
        return workerCageRepository.findAllByWorkerId(workerId)
                                   .stream()
                                   .map(WorkerCage::getCage)
                                   .map(cageMapper::toDto)
                                   .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<WorkerDTO> getCageWorkers(Long cageId) {

        return workerCageRepository.findAllByCageId(cageId)
                                   .stream()
                                   .map(WorkerCage::getWorker)
                                   .map(workerMapper::toDto)
                                   .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public void assignCageToWorker(Long workerId, Long cageId) {
        if (workerCageRepository.existsByWorkerIdAndCageId(workerId, cageId)) {
            return;
        }

        Worker worker = workerRepository.findById(workerId).orElseThrow(() -> new DataExistException(WorkerError.NOT_FOUND_BY_ID, workerId));

        Cage cage = cageRepository.findById(cageId)
                                  .orElseThrow(() -> new DataExistException(CageError.NOT_FOUND_BY_ID, cageId) {
                                  });

        WorkerCage workerCage = new WorkerCage();
        workerCage.setWorker(worker);
        workerCage.setCage(cage);

        workerCageRepository.save(workerCage);
    }

    @Override
    @Transactional
    public void unassignCageFromWorker(Long workerId, Long cageId) {
        workerCageRepository.deleteByWorkerIdAndCageId(workerId, cageId);
    }

    @Override
    @Transactional(readOnly = true)
    public boolean hasWorkerAnyCages(Long workerId) {
        return workerCageRepository.existsByWorkerId(workerId);
    }

    @Override
    @Transactional(readOnly = true)
    public boolean isCageServedByAnyWorker(Long cageId) {
        return workerCageRepository.existsByCageId(cageId);
    }
}
