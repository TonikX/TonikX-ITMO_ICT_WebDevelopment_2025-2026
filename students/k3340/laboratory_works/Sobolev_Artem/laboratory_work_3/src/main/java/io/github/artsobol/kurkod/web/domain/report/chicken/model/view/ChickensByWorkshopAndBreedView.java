package io.github.artsobol.kurkod.web.domain.report.chicken.model.view;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import org.hibernate.annotations.Immutable;

@Entity
@Table(name = "report_chickens_by_workshop_and_breed")
@Immutable
@Getter
public class ChickensByWorkshopAndBreedView {
    @Id
    @Column(name = "workshop_id")
    private Long workshopId;

    @Column(name = "workshop_number")
    private Long workshopNumber;

    @Column(name = "breed_id")
    private Long breedId;

    @Column(name = "breed_name")
    private String breedName;

    @Column(name = "chickens_count")
    private Long chickensCount;
}
