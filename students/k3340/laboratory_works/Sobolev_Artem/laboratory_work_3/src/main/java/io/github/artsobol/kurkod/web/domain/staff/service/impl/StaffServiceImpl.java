package io.github.artsobol.kurkod.web.domain.staff.service.impl;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.logging.LogHelper;
import io.github.artsobol.kurkod.security.facade.SecurityContextFacade;
import io.github.artsobol.kurkod.web.domain.staff.mapper.StaffMapper;
import io.github.artsobol.kurkod.web.domain.staff.error.StaffError;
import io.github.artsobol.kurkod.web.domain.staff.model.dto.StaffDTO;
import io.github.artsobol.kurkod.web.domain.staff.model.entity.Staff;
import io.github.artsobol.kurkod.common.exception.NotFoundException;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPatchRequest;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPostRequest;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPutRequest;
import io.github.artsobol.kurkod.web.domain.staff.repository.StaffRepository;
import io.github.artsobol.kurkod.web.domain.staff.service.api.StaffService;
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
public class StaffServiceImpl implements StaffService {

    private final StaffRepository staffRepository;
    private final StaffMapper staffMapper;
    private final SecurityContextFacade securityContextFacade;

    private String getCurrentUsername() {
        return securityContextFacade.getCurrentUsername();
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public StaffDTO get(Long id) {
        log.debug(ApiLogMessage.GET_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(Staff.class), id);
        return staffMapper.toDto(getStaffById(id));
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public List<StaffDTO> getAll() {
        log.debug(ApiLogMessage.GET_ALL_ENTITIES.getValue(), getCurrentUsername(), LogHelper.getEntityName(Staff.class));
        return staffRepository.findAllByIsActiveTrue().stream()
                .map(staffMapper::toDto)
                .toList();
    }


    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public StaffDTO create(StaffPostRequest request) {
        Staff staff = staffMapper.toEntity(request);
        staff = staffRepository.save(staff);
        log.info(ApiLogMessage.CREATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(staff));
        return staffMapper.toDto(staff);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public StaffDTO replace(Long id, StaffPutRequest request, Long version) {
        Staff staff = getStaffById(id);
        checkVersion(staff.getVersion(), version);
        staffMapper.updateFully(staff, request);
        staff = staffRepository.save(staff);
        log.info(ApiLogMessage.REPLACE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(staff), id);
        return staffMapper.toDto(staff);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public StaffDTO update(Long id, StaffPatchRequest request, Long version) {
        Staff staff = getStaffById(id);
        checkVersion(staff.getVersion(), version);
        staffMapper.updatePartially(staff, request);
        staff = staffRepository.save(staff);
        log.info(ApiLogMessage.UPDATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(staff), id);
        return staffMapper.toDto(staff);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public void delete(Long id, Long version) {
        Staff staff = getStaffById(id);
        checkVersion(staff.getVersion(), version);
        staff.setActive(false);
        log.info(ApiLogMessage.DELETE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(Staff.class), id);
        staffRepository.save(staff);
    }

    protected Staff getStaffById(Long id) {
        return staffRepository.findStaffByIdAndIsActiveTrue(id).orElseThrow(() ->
                new NotFoundException(StaffError.NOT_FOUND_BY_ID, id));
    }
}
