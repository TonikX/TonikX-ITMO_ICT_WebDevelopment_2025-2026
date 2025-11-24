package io.github.artsobol.kurkod.web.domain.report.chicken;


import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface ChickenEggStatsViewRepository extends JpaRepository<ChickenEggStatsView, Long> {

    @Query("""
        SELECT v
        FROM ChickenEggStatsView v
        WHERE (:weight IS NULL OR v.weight = :weight)
          AND (:breedId IS NULL OR v.breedId = :breedId)
          AND (:birthDate IS NULL OR v.birthDate = :birthDate)
        """)
    List<ChickenEggStatsView> findByFilters(@Param("weight") Integer weight,
                                            @Param("breedId") Long breedId,
                                            @Param("birthDate") LocalDate birthDate);
}