package io.github.artsobol.kurkod.web.domain.report.repository;

import io.github.artsobol.kurkod.web.domain.report.breed.model.dto.BreedWorkshopMonthlyReportDTO;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;

@Repository
@RequiredArgsConstructor
public class FarmMonthlyStatsRepository {

    @PersistenceContext private final EntityManager em;

    public List<BreedWorkshopMonthlyReportDTO> findBreedWorkshopMonthlyStats(int year, int month) {
        List<Object[]> rows = em.createNativeQuery("""
                                                   SELECT
                                                       w.id                       AS workshop_id,
                                                       w.workshop_number          AS workshop_number,
                                                       b.id                       AS breed_id,
                                                       b.name                     AS breed_name,
                                                       COUNT(DISTINCT c.id)       AS chickens_count,
                                                       COALESCE(SUM(epm.count), 0) AS eggs_total,
                                                       CASE 
                                                           WHEN COUNT(DISTINCT c.id) = 0 THEN 0
                                                           ELSE COALESCE(SUM(epm.count), 0)::decimal / COUNT(DISTINCT c.id)
                                                       END                        AS avg_eggs_per_chicken
                                                   FROM current_chicken_position ccp
                                                   JOIN chicken c ON c.id = ccp.chicken_id
                                                   JOIN workshop w ON w.id = ccp.workshop_id
                                                   JOIN breed b ON b.id = c.breed_id
                                                   LEFT JOIN egg_production_month epm 
                                                       ON epm.chicken_id = c.id
                                                      AND epm.year = :year
                                                      AND epm.month = :month
                                                   WHERE c.is_active = true
                                                   GROUP BY w.id, w.workshop_number, b.id, b.name
                                                   ORDER BY w.workshop_number, b.name
                                                   """)
                                .setParameter("year", year)
                                .setParameter("month", month)
                                .getResultList();

        return rows.stream().map(this::mapRowToDto).toList();
    }

    private BreedWorkshopMonthlyReportDTO mapRowToDto(Object[] r) {
        Long workshopId = ((Number) r[0]).longValue();
        Integer workshopNumber = ((Number) r[1]).intValue();
        Long breedId = ((Number) r[2]).longValue();
        String breedName = (String) r[3];
        Long chickensCount = ((Number) r[4]).longValue();
        Long eggsTotal = ((Number) r[5]).longValue();
        BigDecimal avgEggsPerChicken = (r[6] instanceof BigDecimal bd)
                                       ? bd
                                       : BigDecimal.valueOf(((Number) r[6]).doubleValue());

        return new BreedWorkshopMonthlyReportDTO(workshopId,
                                                 workshopNumber,
                                                 breedId,
                                                 breedName,
                                                 chickensCount,
                                                 eggsTotal,
                                                 avgEggsPerChicken);
    }
}

