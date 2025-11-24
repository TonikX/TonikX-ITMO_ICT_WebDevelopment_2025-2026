package io.github.artsobol.kurkod.web.domain.workshop.model.entity;

import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import io.github.artsobol.kurkod.web.domain.rows.model.entity.Rows;
import jakarta.persistence.*;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Entity
@Table(name = "workshop")
public class Workshop extends BaseEntity {

    @Positive
    @Column(nullable = false, unique = true, name = "workshop_number")
    private Integer workshopNumber;

    @OneToMany(mappedBy = "workshop", fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Rows> rows;
}
