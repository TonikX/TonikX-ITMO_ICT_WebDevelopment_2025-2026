package io.github.artsobol.kurkod.web.domain.breed.model.entity;

import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import io.github.artsobol.kurkod.web.domain.diet.model.entity.Diet;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.*;

import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "breed")
@Getter
@Setter
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@AllArgsConstructor
public class Breed extends BaseEntity {

    @NotBlank
    @Size(min = 2, max = 20, message = "Name should be between 2 and 20 characters")
    @Column(nullable = false, unique = true)
    private String name;

    @NotNull
    @Column(nullable = false, name = "eggs_number")
    private Integer eggsNumber;

    @NotNull
    @Column(nullable = false)
    private Integer weight;

    @ManyToMany(mappedBy = "breeds")
    private Set<Diet> diets = new HashSet<>();
}
