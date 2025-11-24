package io.github.artsobol.kurkod.web.domain.dismissal.model.entity;

import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import io.github.artsobol.kurkod.web.domain.worker.model.entity.Worker;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;

@Entity
@Getter
@Setter
@Table(name = "dismissal")
@NoArgsConstructor
@AllArgsConstructor
public class Dismissal extends BaseEntity {

    @NotNull
    @Column(nullable = false, name = "dismissal_date")
    private LocalDate dismissalDate;

    @NotBlank
    @Column(nullable = false)
    private String reason;

    @ManyToOne(optional = false)
    @JoinColumn(name = "worker_id", nullable = false)
    private Worker worker;

    @ManyToOne(optional = false)
    @JoinColumn(name = "who_dismiss_id", nullable = false)
    private Worker whoDismiss;
}
