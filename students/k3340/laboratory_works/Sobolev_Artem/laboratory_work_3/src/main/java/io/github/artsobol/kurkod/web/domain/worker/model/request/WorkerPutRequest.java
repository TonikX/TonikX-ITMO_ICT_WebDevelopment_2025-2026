package io.github.artsobol.kurkod.web.domain.worker.model.request;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class WorkerPutRequest {

    @NotNull
    @Size(min = 2, max = 50, message = "First name should be between 2 and 50 characters")
    private String firstName;

    @NotNull
    @Size(min = 2, max = 50, message = "First name should be between 2 and 50 characters")
    private String lastName;

    @NotNull
    @Size(max = 30, message = "Patronymic name should be less then 30 characters")
    private String patronymic;
}
