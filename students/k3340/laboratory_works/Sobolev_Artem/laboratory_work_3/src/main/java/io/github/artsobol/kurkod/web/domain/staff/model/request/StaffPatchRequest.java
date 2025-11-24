package io.github.artsobol.kurkod.web.domain.staff.model.request;

import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class StaffPatchRequest {

    @Size(min = 2, max = 50, message = "Name should be between 2 and 50 characters")
    private String position;
}
