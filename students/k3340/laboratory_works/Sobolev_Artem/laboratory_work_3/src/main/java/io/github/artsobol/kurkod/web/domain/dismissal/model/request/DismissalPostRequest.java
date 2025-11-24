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
public class DismissalPostRequest {

    @NotNull
    @PastOrPresent
    private LocalDate dismissalDate;

    @Size(max=200)
    private String reason;

    @NotNull
    @Positive
    private Long workerId;
}
