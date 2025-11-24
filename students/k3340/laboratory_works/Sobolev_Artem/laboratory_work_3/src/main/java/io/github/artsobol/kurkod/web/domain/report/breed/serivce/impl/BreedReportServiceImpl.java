package io.github.artsobol.kurkod.web.domain.report.breed.serivce.impl;

import io.github.artsobol.kurkod.web.domain.report.breed.model.dto.BreedEggDiffReportDTO;
import io.github.artsobol.kurkod.web.domain.report.breed.model.view.BreedEggDiffReport;
import io.github.artsobol.kurkod.web.domain.report.breed.repository.BreedEggDiffReportRepository;
import io.github.artsobol.kurkod.web.domain.report.breed.serivce.api.BreedReportService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
@Transactional(readOnly = true)
public class BreedReportServiceImpl implements BreedReportService {

    private final BreedEggDiffReportRepository repository;

    @Override
    public List<BreedEggDiffReportDTO> getEggDiff() {
        return repository.findAll()
                         .stream()
                         .map(this::toDto)
                         .toList();
    }

    private BreedEggDiffReportDTO toDto(BreedEggDiffReport entity) {
        return new BreedEggDiffReportDTO(
                entity.getBreedId(),
                entity.getBreedName(),
                entity.getBreedAvgEggs(),
                entity.getFarmAvgEggs(),
                entity.getDiffEggs()
        );
    }
}