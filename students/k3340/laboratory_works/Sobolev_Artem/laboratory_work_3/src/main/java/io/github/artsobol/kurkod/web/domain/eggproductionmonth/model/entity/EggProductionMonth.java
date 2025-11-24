package io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.entity;

import io.github.artsobol.kurkod.web.domain.chicken.model.entity.Chicken;
import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.*;

@Getter
@Setter
@Entity
@Table(name = "egg_production_month",
       uniqueConstraints = @UniqueConstraint(name = "uq_egg_production_month_chicken_id_month_year",
                                             columnNames = {"chicken_id", "month", "year"}))
@NoArgsConstructor
@AllArgsConstructor
public class EggProductionMonth extends BaseEntity {

    @NotNull
    @Positive
    @Column(nullable = false)
    private Integer year;

    @Min(1)
    @Max(12)
    @NotNull
    @Column(nullable = false)
    private Integer month;

    @NotNull
    @Positive
    @Column(nullable = false)
    private Integer count;

    @ManyToOne(fetch = FetchType.LAZY, optional = false) @JoinColumn(name = "chicken_id", nullable = false)
    private Chicken chicken;
}
