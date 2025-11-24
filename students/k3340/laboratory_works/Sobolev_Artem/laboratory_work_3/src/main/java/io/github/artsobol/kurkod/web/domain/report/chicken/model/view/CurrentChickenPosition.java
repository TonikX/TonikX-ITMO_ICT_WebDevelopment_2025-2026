package io.github.artsobol.kurkod.web.domain.report.chicken.model.view;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import org.hibernate.annotations.Immutable;

@Entity
@Table(name = "current_chicken_position")
@Immutable
@Getter
public class CurrentChickenPosition {

    @Id
    @Column(name = "chicken_id")
    private Long chickenId;

    @Column(name = "cage_id")
    private Long cageId;

    @Column(name = "row_id")
    private Long rowId;

    @Column(name = "workshop_id")
    private Long workshopId;
}
