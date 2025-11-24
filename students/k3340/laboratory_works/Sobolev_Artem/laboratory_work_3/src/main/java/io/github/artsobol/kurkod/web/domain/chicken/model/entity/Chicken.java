package io.github.artsobol.kurkod.web.domain.chicken.model.entity;

import io.github.artsobol.kurkod.web.domain.breed.model.entity.Breed;
import io.github.artsobol.kurkod.web.domain.cage.model.entity.Cage;
import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.*;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
@Table(name = "chicken")
public class Chicken extends BaseEntity {

    @NotBlank
    @Column(length = 30, nullable = false)
    private String name;

    @NotNull
    @Column(nullable = false)
    private Integer weight;

    @NotNull
    @Column(nullable = false, name = "birth_date")
    private LocalDate birthDate;

    @NotNull
    @ManyToOne
    @JoinColumn(name = "breed_id", nullable = false)
    private Breed breed;

    @NotNull
    @ManyToOne
    @JoinColumn(name = "cage_id", nullable = false)
    private Cage cage;
}
