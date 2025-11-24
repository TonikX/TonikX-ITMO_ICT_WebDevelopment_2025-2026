package io.github.artsobol.kurkod.web.domain.worker.model.entity;

import io.github.artsobol.kurkod.web.domain.cage.model.entity.Cage;
import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "worker")
@Getter
@Setter
public class Worker extends BaseEntity {

    @NotBlank
    @Column(nullable = false, length = 30)
    @Size(max = 30, message = "First name should be between 1 and 50 characters")
    private String firstName;

    @NotBlank
    @Column(nullable = false, length = 30)
    @Size(max = 30, message = "Last name should be between 1 and 50 characters")
    private String lastName;

    @Column(length = 30)
    @Size(max = 30, message = "Patronymic should be less than 30 characters")
    private String patronymic;

    @OneToMany(mappedBy = "worker", fetch = FetchType.LAZY)
    private Set<WorkerCage> workerCages = new HashSet<>();
}
