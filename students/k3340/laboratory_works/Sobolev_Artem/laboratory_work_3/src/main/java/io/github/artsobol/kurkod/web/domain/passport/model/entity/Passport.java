package io.github.artsobol.kurkod.web.domain.passport.model.entity;

import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import io.github.artsobol.kurkod.web.domain.worker.model.entity.Worker;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;


@Entity
@Table(name = "passport", uniqueConstraints = @UniqueConstraint(columnNames = {"series", "number"}, name = "uq_passport_series_number"))
@Getter
@Setter
@NoArgsConstructor
public class Passport extends BaseEntity {

    @Column(length = 4, nullable = false)
    @Pattern(regexp = "^[0-9]{4}$", message = "Invalid passport series")
    private String series;

    @Column(length = 6, nullable = false)
    @Pattern(regexp = "^[0-9]{6}$", message = "Invalid passport number")
    private String number;

    @NotNull
    @OneToOne(optional = false)
    @JoinColumn(name = "worker_id", nullable = false)
    private Worker worker;
}
