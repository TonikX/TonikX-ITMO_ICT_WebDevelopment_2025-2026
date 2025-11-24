package io.github.artsobol.kurkod.web.domain.chicken.model.request;

import jakarta.validation.constraints.Past;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChickenPatchRequest {

    private String name;

    @Positive
    private Integer weight;

    @Past
    private LocalDate birthDate;

    private Long breedId;

    private Long cageId;
}
