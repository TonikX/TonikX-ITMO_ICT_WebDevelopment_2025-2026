package io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.request;

import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class EggProductionMonthPatchRequest {

    @Positive
    private Integer count;
}
