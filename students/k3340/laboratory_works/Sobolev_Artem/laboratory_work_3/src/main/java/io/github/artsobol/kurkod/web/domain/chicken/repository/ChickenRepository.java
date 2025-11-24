package io.github.artsobol.kurkod.web.domain.chicken.repository;

import io.github.artsobol.kurkod.web.domain.chicken.model.entity.Chicken;
import io.github.artsobol.kurkod.web.domain.report.farm.projection.BreedWorkshopMonthlyProjection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface ChickenRepository extends JpaRepository<Chicken, Long> {

    Optional<Chicken> findChickenByIdAndIsActiveTrue(Long id);

    List<Chicken> findAllByIsActiveTrue();

    @Query("select count(c) from Chicken c where c.isActive = true")
    long countActiveChickens();

    @Query(value = """
                   SELECT
                       w.id               AS workshop_id,
                       w.workshop_number  AS workshop_number,
                       b.id               AS breed_id,
                       b.name             AS breed_name,
                       COUNT(DISTINCT c.id)            AS chickens_count,
                       COALESCE(SUM(epm.count), 0)     AS eggs_total,
                       CASE
                           WHEN COUNT(DISTINCT c.id) = 0 THEN 0
                           ELSE ROUND(
                               COALESCE(SUM(epm.count), 0)::numeric
                               / COUNT(DISTINCT c.id), 2
                           )
                       END AS avg_eggs_per_chicken
                   FROM chicken c
                   JOIN breed b
                     ON b.id = c.breed_id
                   JOIN cage cg
                     ON cg.id = c.cage_id
                   JOIN "rows" r
                     ON r.id = cg.row_id
                   JOIN workshop w
                     ON w.id = r.workshop_id
                   JOIN egg_production_month epm
                     ON epm.chicken_id = c.id
                   WHERE c.is_active = true
                     AND epm.year  = :year
                     AND epm.month = :month
                   GROUP BY
                       w.id, w.workshop_number,
                       b.id, b.name
                   ORDER BY
                       w.workshop_number,
                       b.name
                   """, nativeQuery = true)
    java.util.List<BreedWorkshopMonthlyProjection> findBreedWorkshopMonthlyStats(
            @Param("year") int year,
            @Param("month") int month);
}
