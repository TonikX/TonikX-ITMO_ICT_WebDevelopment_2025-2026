package io.github.artsobol.kurkod.web.domain.report.breed.model.view;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.Immutable;

import java.math.BigDecimal;

@Entity
@Table(name = "breed_egg_diff_report")
@Immutable
@Getter
@Setter
public class BreedEggDiffReport {

    @Id
    @Column(name = "breed_id")
    private Long breedId;

    @Column(name = "breed_name")
    private String breedName;

    @Column(name = "breed_avg_eggs")
    private BigDecimal breedAvgEggs;

    @Column(name = "farm_avg_eggs")
    private BigDecimal farmAvgEggs;

    @Column(name = "diff_eggs")
    private BigDecimal diffEggs;
}
