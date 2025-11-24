package io.github.artsobol.kurkod.web.domain.report.chicken.service.api;

import io.github.artsobol.kurkod.web.domain.report.chicken.model.dto.ChickenEggStatsDTO;
import io.github.artsobol.kurkod.web.domain.report.chicken.model.dto.ChickensByWorkshopAndBreedDTO;
import io.github.artsobol.kurkod.web.domain.report.chicken.model.dto.WorkshopBreedTopDTO;

import java.time.LocalDate;
import java.util.List;

public interface ChickenReportService {

    List<ChickensByWorkshopAndBreedDTO> getChickensByWorkshopAndBreed();

    WorkshopBreedTopDTO getTopWorkshopByBreed(Long breedId);

    List<ChickenEggStatsDTO> getEggStats(Integer weight, Long breedId, LocalDate birthDate);
}