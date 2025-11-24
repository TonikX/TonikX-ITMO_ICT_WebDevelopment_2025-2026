package io.github.artsobol.kurkod.web.domain.report.chicken;

import io.github.artsobol.kurkod.web.domain.report.chicken.model.view.ChickensByWorkshopAndBreedView;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ChickensByWorkshopAndBreedViewRepository
        extends JpaRepository<ChickensByWorkshopAndBreedView, Long> {

    java.util.List<ChickensByWorkshopAndBreedView> findByBreedIdOrderByChickensCountDesc(Long breedId);
}