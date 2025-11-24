package io.github.artsobol.kurkod.web.domain.passport.model.request;

import jakarta.validation.constraints.Pattern;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PassportPatchRequest {

    @Pattern(regexp = "^[0-9]{4}$", message = "Invalid passport series")
    private String series;

    @Pattern(regexp = "^[0-9]{6}$", message = "Invalid passport number")
    private String number;
}