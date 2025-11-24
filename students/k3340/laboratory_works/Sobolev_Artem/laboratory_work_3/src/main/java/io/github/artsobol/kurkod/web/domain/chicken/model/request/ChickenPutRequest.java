package io.github.artsobol.kurkod.web.domain.chicken.model.request;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ChickenPutRequest {

    @NotNull
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
