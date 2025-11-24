package io.github.artsobol.kurkod.web.domain.report.breed.repository;

import io.github.artsobol.kurkod.web.domain.report.breed.model.view.BreedEggDiffReport;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface BreedEggDiffReportRepository extends JpaRepository<BreedEggDiffReport, Long> {
}
