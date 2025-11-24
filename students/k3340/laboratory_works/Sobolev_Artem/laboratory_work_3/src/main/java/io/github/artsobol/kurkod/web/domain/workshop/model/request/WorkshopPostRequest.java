package io.github.artsobol.kurkod.web.domain.workshop.model.request;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@RequiredArgsConstructor
public class WorkshopPostRequest {

    @NotNull
    @Positive
    private Integer workshopNumber;
}
