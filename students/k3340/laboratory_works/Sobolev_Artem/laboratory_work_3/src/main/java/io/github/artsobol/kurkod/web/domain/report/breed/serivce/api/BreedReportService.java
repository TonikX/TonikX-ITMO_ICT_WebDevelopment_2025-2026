package io.github.artsobol.kurkod.web.domain.report.breed.serivce.api;

import io.github.artsobol.kurkod.web.domain.report.breed.model.dto.BreedEggDiffReportDTO;

import java.util.List;

public interface BreedReportService {

    List<BreedEggDiffReportDTO> getEggDiff();
}
