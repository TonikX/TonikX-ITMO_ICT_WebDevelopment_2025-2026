package io.github.artsobol.kurkod.web.domain.dismissal.model.request;

import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class DismissalPutRequest {

    @NotNull
    @PastOrPresent
    private LocalDate dismissalDate;

    @Size(min=2, max=200)
    private String reason;
}
