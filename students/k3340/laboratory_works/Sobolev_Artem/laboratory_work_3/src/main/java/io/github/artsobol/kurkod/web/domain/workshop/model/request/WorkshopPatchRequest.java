package io.github.artsobol.kurkod.web.domain.workshop.model.request;

import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@RequiredArgsConstructor
public class WorkshopPatchRequest {

    @Positive
    private Integer workshopNumber;
}
