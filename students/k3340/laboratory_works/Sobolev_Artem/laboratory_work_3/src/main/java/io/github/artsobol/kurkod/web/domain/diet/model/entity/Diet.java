package io.github.artsobol.kurkod.web.domain.diet.model.entity;

import io.github.artsobol.kurkod.web.domain.breed.model.entity.Breed;
import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import io.github.artsobol.kurkod.web.domain.common.model.Season;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

@Entity
@Getter
@Setter
@Table(name = "diet")
public class Diet extends BaseEntity {

    @NotBlank @Size(min = 2, max = 30, message = "Title should be between 2 and 30 characters")
    @Column(nullable = false, unique = true) private String title;

    @NotBlank @Size(min = 2, max = 10, message = "Code should be between 2 and 10 characters")
    @Column(nullable = false, unique = true) private String code;

    private String description;

    @Enumerated(EnumType.STRING) @Column(name = "season", nullable = false, length = 6) private Season season;

    @ManyToMany
    @JoinTable(name = "breed_diet",
               joinColumns = @JoinColumn(name = "diet_id"),
               inverseJoinColumns = @JoinColumn(name = "breed_id")) private Set<Breed> breeds = new HashSet<>();

    public void addBreed(@NonNull Breed breed) {
        if (breeds.add(breed)) {
            breed.getDiets().add(this);
        }
    }

    public void removeBreed(Breed breed) {
        if (breeds.remove(breed)) {
            breed.getDiets().remove(this);
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof Diet other)) {
            return false;
        }
        return id != null && id.equals(other.id);
    }

    @Override
    public int hashCode() {
        return 31;
    }
}
