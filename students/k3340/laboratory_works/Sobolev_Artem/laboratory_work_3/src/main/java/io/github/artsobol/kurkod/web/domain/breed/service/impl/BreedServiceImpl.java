package io.github.artsobol.kurkod.web.domain.breed.service.impl;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.exception.DataExistException;

import static io.github.artsobol.kurkod.common.util.VersionUtils.checkVersion;

import io.github.artsobol.kurkod.common.logging.LogHelper;
import io.github.artsobol.kurkod.security.facade.SecurityContextFacade;
import io.github.artsobol.kurkod.web.domain.breed.mapper.BreedMapper;
import io.github.artsobol.kurkod.web.domain.breed.error.BreedError;
import io.github.artsobol.kurkod.web.domain.breed.model.dto.BreedDTO;
import io.github.artsobol.kurkod.web.domain.breed.model.entity.Breed;
import io.github.artsobol.kurkod.web.domain.breed.model.request.BreedPatchRequest;
import io.github.artsobol.kurkod.web.domain.breed.model.request.BreedPostRequest;
import io.github.artsobol.kurkod.web.domain.breed.model.request.BreedPutRequest;
import io.github.artsobol.kurkod.web.domain.breed.repository.BreedRepository;
import io.github.artsobol.kurkod.web.domain.breed.service.api.BreedService;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Slf4j
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class BreedServiceImpl implements BreedService {

    private final BreedRepository breedRepository;
    private final BreedLookupService breedLookupService;
    private final BreedMapper breedMapper;
    private final SecurityContextFacade securityContextFacade;

    private String getCurrentUsername() {
        return securityContextFacade.getCurrentUsername();
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public BreedDTO create(BreedPostRequest breedPostRequest) {
        ensureNotExists(breedPostRequest.getName());

        Breed breed = breedMapper.toEntity(breedPostRequest);
        breed = breedRepository.save(breed);

        log.info(ApiLogMessage.CREATE_ENTITY.getValue(),
                 getCurrentUsername(),
                 LogHelper.getEntityName(breed),
                 breed.getId());
        return breedMapper.toDto(breed);
    }

    @Override
    public BreedDTO get(@NotNull Long id) {
        log.debug(ApiLogMessage.GET_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(Breed.class), id);
        return breedMapper.toDto(breedLookupService.getBreedByIdOrThrow(id));
    }

    @Override
    public List<BreedDTO> getAll() {
        log.debug(ApiLogMessage.GET_ALL_ENTITIES.getValue(), getCurrentUsername());
        return breedRepository.findAllByIsActiveTrue().stream().map(breedMapper::toDto).toList();
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public BreedDTO replace(Long id, BreedPutRequest request, Long version) {
        Breed breed = breedLookupService.getBreedByIdOrThrow(id);
        checkVersion(breed.getVersion(), version);
        breedMapper.updateFully(breed, request);
        breed = breedRepository.save(breed);

        log.info(ApiLogMessage.REPLACE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(breed), id);
        return breedMapper.toDto(breed);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public BreedDTO update(Long id, BreedPatchRequest breedPatchRequest, Long version) {
        Breed breed = breedLookupService.getBreedByIdOrThrow(id);
        checkVersion(breed.getVersion(), version);
        breedMapper.updatePartially(breed, breedPatchRequest);
        breed = breedRepository.save(breed);

        log.info(ApiLogMessage.UPDATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(breed), id);
        return breedMapper.toDto(breed);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public void delete(Long id, Long version) {
        Breed breed = breedLookupService.getBreedByIdOrThrow(id);
        checkVersion(breed.getVersion(), version);
        breed.setActive(false);

        log.info(ApiLogMessage.DELETE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(breed), id);
        breedRepository.save(breed);
    }

    protected void ensureNotExists(String name) {
        if (existsByName(name)) {
            log.info(BreedError.ALREADY_EXISTS.format(name));
            throw new DataExistException(BreedError.ALREADY_EXISTS, name);
        }
    }

    protected boolean existsByName(String name) {
        return breedRepository.existsByNameAndIsActiveTrue(name);
    }

}
