package io.github.artsobol.kurkod.web.domain.breed.model.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.*;

import java.io.Serializable;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class BreedPostRequest {

    @NotBlank
    private String name;

    @NotNull
    @Positive
    private Integer eggsNumber;

    @NotNull
    @Positive
    private Integer weight;
}
