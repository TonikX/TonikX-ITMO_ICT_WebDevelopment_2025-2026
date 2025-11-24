package io.github.artsobol.kurkod.web.domain.rows.model.entity;

import io.github.artsobol.kurkod.web.domain.cage.model.entity.Cage;
import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import io.github.artsobol.kurkod.web.domain.workshop.model.entity.Workshop;
import jakarta.persistence.*;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "rows",
       uniqueConstraints = @UniqueConstraint(name = "uq_rows_workshop_id_row_number",
                                             columnNames = {"workshop_id", "row_number"}))
@AllArgsConstructor
@NoArgsConstructor
public class Rows extends BaseEntity {
    @Positive @Column(nullable = false, name = "row_number") private Integer rowNumber;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "workshop_id", nullable = false, referencedColumnName = "id") private Workshop workshop;

    @OneToMany(mappedBy = "row", fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Cage> cages;
}
