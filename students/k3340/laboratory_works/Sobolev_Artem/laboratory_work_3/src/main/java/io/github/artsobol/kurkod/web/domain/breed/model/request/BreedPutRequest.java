package io.github.artsobol.kurkod.web.domain.breed.model.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.security.core.parameters.P;

import java.io.Serializable;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class BreedPutRequest {

    @NotBlank
    private String name;

    @NotNull
    @Positive
    private Integer eggsNumber;

    @NotNull
    @Positive
    private Integer weight;
}
