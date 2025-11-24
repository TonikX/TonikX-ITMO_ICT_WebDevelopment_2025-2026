package io.github.artsobol.kurkod.web.domain.cage.repository;

import io.github.artsobol.kurkod.web.domain.cage.model.entity.Cage;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface CageRepository extends JpaRepository<Cage, Long> {

    Optional<Cage> findByRow_IdAndCageNumberAndIsActiveTrue(Long rowId, Integer cageNumber);

    List<Cage> findAllByRow_IdAndIsActiveTrueOrderByCageNumberAsc(Long rowId);

    boolean existsByRow_IdAndCageNumberAndIsActiveTrue(Long rowId, Integer cageNumber);
}
