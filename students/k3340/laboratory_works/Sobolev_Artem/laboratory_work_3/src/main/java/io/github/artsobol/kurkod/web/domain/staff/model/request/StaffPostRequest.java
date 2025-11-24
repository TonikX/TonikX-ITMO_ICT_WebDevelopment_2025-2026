package io.github.artsobol.kurkod.web.domain.staff.model.request;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class StaffPostRequest {

    @NotNull
    @Size(min = 2, max = 50, message = "Name should be between 2 and 50 characters")
    private String position;
}
