package io.github.artsobol.kurkod.web.domain.diet.repository;

import io.github.artsobol.kurkod.web.domain.diet.model.entity.Diet;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface DietRepository extends JpaRepository<Diet, Long> {

    Optional<Diet> findDietByIdAndIsActiveTrue(Long id);

    List<Diet> findAllByIsActiveTrue();

    boolean existsByCodeAndIsActiveTrue(String code);
}
