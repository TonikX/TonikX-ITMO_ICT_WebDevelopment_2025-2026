package io.github.artsobol.kurkod.web.domain.passport.service.impl;


import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.logging.LogHelper;
import io.github.artsobol.kurkod.security.facade.SecurityContextFacade;
import io.github.artsobol.kurkod.web.domain.passport.mapper.PassportMapper;
import io.github.artsobol.kurkod.web.domain.passport.error.PassportError;
import io.github.artsobol.kurkod.web.domain.passport.service.api.PassportService;
import io.github.artsobol.kurkod.web.domain.worker.error.WorkerError;
import io.github.artsobol.kurkod.web.domain.passport.model.dto.PassportDTO;
import io.github.artsobol.kurkod.web.domain.passport.model.entity.Passport;
import io.github.artsobol.kurkod.web.domain.worker.model.entity.Worker;
import io.github.artsobol.kurkod.common.exception.NotFoundException;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPatchRequest;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPostRequest;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPutRequest;
import io.github.artsobol.kurkod.web.domain.passport.repository.PassportRepository;
import io.github.artsobol.kurkod.web.domain.worker.repository.WorkerRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import static io.github.artsobol.kurkod.common.util.VersionUtils.checkVersion;

@Slf4j
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class PassportServiceImpl implements PassportService {

    private final PassportRepository passportRepository;
    private final PassportMapper passportMapper;
    private final WorkerRepository workerRepository;
    private final SecurityContextFacade securityContextFacade;

    private String getCurrentUsername() {
        return securityContextFacade.getCurrentUsername();
    }

    @Override
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public PassportDTO get(Long workerId) {
        log.debug(ApiLogMessage.GET_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(Passport.class), workerId);
        return passportMapper.toDto(getPassportByWorkerId(workerId));
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public PassportDTO create(Long workerId, PassportPostRequest passportPostRequest) {
        Worker worker = workerRepository.findWorkerByIdAndIsActiveTrue(workerId).orElseThrow(
                () -> new NotFoundException(WorkerError.NOT_FOUND_BY_ID, workerId)
        );

        passportRepository.findPassportByWorkerIdAndIsActiveTrue(workerId)
                .ifPresent(p -> {
                    throw new IllegalStateException("Worker already has an active passport");
                });

        Passport passport = passportMapper.toEntity(passportPostRequest);
        passport.setWorker(worker);
        passport.setActive(true);
        passport = passportRepository.save(passport);
        log.info(ApiLogMessage.CREATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(passport), workerId);
        return passportMapper.toDto(passport);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public PassportDTO replace(Long workerId, PassportPutRequest request, Long version) {
        Passport passport = getPassportByWorkerId(workerId);
        checkVersion(passport.getVersion(), version);
        passportMapper.updateFully(passport, request);
        passport = passportRepository.save(passport);
        log.info(ApiLogMessage.REPLACE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(passport), workerId);
        return passportMapper.toDto(passport);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public PassportDTO update(Long workerId, PassportPatchRequest request, Long version) {
        Passport passport = getPassportByWorkerId(workerId);
        checkVersion(passport.getVersion(), version);
        passportMapper.updatePartially(passport, request);
        passport = passportRepository.save(passport);
        log.info(ApiLogMessage.UPDATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(passport), workerId);
        return passportMapper.toDto(passport);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public void delete(Long workerId, Long version) {
        Passport passport = getPassportByWorkerId(workerId);
        checkVersion(passport.getVersion(), version);
        passport.setActive(false);
        log.info(ApiLogMessage.DELETE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(Passport.class), workerId);
        passportRepository.save(passport);
    }

    protected Passport getPassportByWorkerId(Long workerId) {
        return passportRepository.findPassportByWorkerIdAndIsActiveTrue(workerId).orElseThrow(
                () -> new NotFoundException(PassportError.NOT_FOUND_BY_WORKER_ID, workerId)
        );
    }
}
