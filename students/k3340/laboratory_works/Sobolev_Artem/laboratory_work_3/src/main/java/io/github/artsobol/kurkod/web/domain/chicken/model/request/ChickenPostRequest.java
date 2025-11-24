package io.github.artsobol.kurkod.web.domain.chicken.model.request;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.time.LocalDate;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ChickenPostRequest implements Serializable {

    private String name;

    @NotNull
    private Integer weight;

    @NotNull
    private LocalDate birthDate;

    @NotNull
    private Long breedId;

    @NotNull
    private Long cageId;
}
