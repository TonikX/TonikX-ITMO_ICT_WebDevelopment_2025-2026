package io.github.artsobol.kurkod.web.domain.cage.model.request;

import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class CagePatchRequest {

    @Positive
    private Integer cageNumber;
}
