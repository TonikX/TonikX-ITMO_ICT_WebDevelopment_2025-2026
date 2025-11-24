package io.github.artsobol.kurkod.web.domain.eggproductionmonth.repository;

import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.entity.EggProductionMonth;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface EggProductionMonthRepository extends JpaRepository<EggProductionMonth, Long> {

    List<EggProductionMonth> findAllByChicken_IdAndIsActiveTrue(Long chickenId);

    List<EggProductionMonth> findAllByChicken_IdAndYearAndIsActiveTrue(Long chickenId, int year);

    Optional<EggProductionMonth> findByChicken_IdAndMonthAndYearAndIsActiveTrue(Long chickenId, int month, int year);

    boolean existsByChicken_IdAndMonthAndYearAndIsActiveTrue(Long chickenId, int month, int year);

    @Query("""
        SELECT COALESCE(SUM(e.count), 0)
        FROM EggProductionMonth e
        WHERE e.year = :year AND e.month = :month
    """)
    Long countEggsByMonth(@Param("year") int year, @Param("month") int month);
}
