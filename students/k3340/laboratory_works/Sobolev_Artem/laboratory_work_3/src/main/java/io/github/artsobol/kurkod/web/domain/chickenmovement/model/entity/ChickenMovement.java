package io.github.artsobol.kurkod.web.domain.chickenmovement.model.entity;

import io.github.artsobol.kurkod.web.domain.cage.model.entity.Cage;
import io.github.artsobol.kurkod.web.domain.chicken.model.entity.Chicken;
import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.sql.Timestamp;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.OffsetDateTime;

@Entity
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "chicken_movement")
public class ChickenMovement extends BaseEntity {

    @NotNull @Column(nullable = false, name = "moved_at") private OffsetDateTime movedAt = OffsetDateTime.now();

    @ManyToOne(fetch = FetchType.LAZY, optional = false) @JoinColumn(name = "chicken_id", nullable = false)
    private Chicken chicken;

    @ManyToOne(fetch = FetchType.LAZY) @JoinColumn(name = "from_cage_id") private Cage fromCage;

    @ManyToOne(fetch = FetchType.LAZY, optional = false) @JoinColumn(name = "to_cage_id", nullable = false)
    private Cage toCage;
}
