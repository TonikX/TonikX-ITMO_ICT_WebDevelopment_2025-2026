package io.github.artsobol.kurkod.web.domain.workshop.service.impl;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.exception.DataExistException;
import io.github.artsobol.kurkod.common.exception.NotFoundException;
import io.github.artsobol.kurkod.common.logging.LogHelper;
import io.github.artsobol.kurkod.security.facade.SecurityContextFacade;
import io.github.artsobol.kurkod.web.domain.workshop.error.WorkshopError;
import io.github.artsobol.kurkod.web.domain.workshop.mapper.WorkshopMapper;
import io.github.artsobol.kurkod.web.domain.workshop.model.dto.WorkshopDTO;
import io.github.artsobol.kurkod.web.domain.workshop.model.entity.Workshop;
import io.github.artsobol.kurkod.web.domain.workshop.model.request.WorkshopPatchRequest;
import io.github.artsobol.kurkod.web.domain.workshop.model.request.WorkshopPostRequest;
import io.github.artsobol.kurkod.web.domain.workshop.model.request.WorkshopPutRequest;
import io.github.artsobol.kurkod.web.domain.workshop.repository.WorkshopRepository;
import io.github.artsobol.kurkod.web.domain.workshop.service.api.WorkshopService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

import static io.github.artsobol.kurkod.common.util.VersionUtils.checkVersion;

@Slf4j
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class WorkshopServiceImpl implements WorkshopService {

    private final WorkshopRepository workshopRepository;
    private final SecurityContextFacade securityContextFacade;
    private final WorkshopMapper workshopMapper;

    private String getCurrentUsername() {
        return securityContextFacade.getCurrentUsername();
    }


    @Override
    public WorkshopDTO get(Long id) {
        log.debug(ApiLogMessage.GET_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(Workshop.class), id);
        return workshopMapper.toDto(getWorkshopById(id));
    }

    @Override
    public List<WorkshopDTO> getAll() {
        log.debug(ApiLogMessage.GET_ALL_ENTITIES.getValue(), getCurrentUsername(), LogHelper.getEntityName(Workshop.class));
        return workshopRepository.findAllByIsActiveTrue().stream()
                .map(workshopMapper::toDto)
                .toList();
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public WorkshopDTO create(WorkshopPostRequest request) {
        Integer workshopNumber = request.getWorkshopNumber();
        ensureNotExists(workshopNumber);

        Workshop workshop = workshopMapper.toEntity(request);
        workshopRepository.save(workshop);
        log.info(ApiLogMessage.CREATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(workshop), workshop.getId());
        return workshopMapper.toDto(workshop);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public WorkshopDTO update(Long id, WorkshopPatchRequest request, Long version) {
        Workshop workshop = getWorkshopById(id);
        checkVersion(workshop.getVersion(), version);
        Integer newWorkshopNumber = request.getWorkshopNumber();
        if (newWorkshopNumber != null && !newWorkshopNumber.equals(workshop.getWorkshopNumber())) {
            ensureNotExists(newWorkshopNumber);
        }

        workshopMapper.update(workshop, request);
        workshopRepository.save(workshop);

        log.info(ApiLogMessage.UPDATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(workshop), id);
        return workshopMapper.toDto(workshop);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public WorkshopDTO replace(Long id, WorkshopPutRequest request, Long version) {
        Workshop workshop = getWorkshopById(id);
        checkVersion(workshop.getVersion(), version);
        Integer newWorkshopNumber = request.getWorkshopNumber();
        if (newWorkshopNumber != null && !newWorkshopNumber.equals(workshop.getWorkshopNumber())) {
            ensureNotExists(newWorkshopNumber);
        }

        workshopMapper.replace(workshop, request);
        log.info(ApiLogMessage.REPLACE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(workshop), id);
        return workshopMapper.toDto(workshopRepository.save(workshop));
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public void delete(Long id, Long version) {
        Workshop workshop = getWorkshopById(id);
        checkVersion(workshop.getVersion(), version);
        log.info(ApiLogMessage.DELETE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(Workshop.class), id);
        workshop.setActive(false);
    }

    protected Workshop getWorkshopById(Long id) {
        return workshopRepository.findWorkshopByIdAndIsActiveTrue(id).orElseThrow(
                () -> new NotFoundException(WorkshopError.NOT_FOUND_BY_ID, id)
        );
    }

    protected void ensureNotExists(Integer id) {
        if (existsById(id)){
            log.info(WorkshopError.ALREADY_EXISTS.format(id));
            throw new DataExistException(WorkshopError.ALREADY_EXISTS, id);
        }
    }

    protected boolean existsById(Integer id){
        return workshopRepository.existsByWorkshopNumberAndIsActiveTrue(id);
    }
}
