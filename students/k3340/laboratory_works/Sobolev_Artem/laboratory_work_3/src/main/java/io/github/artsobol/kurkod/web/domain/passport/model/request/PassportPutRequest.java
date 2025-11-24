package io.github.artsobol.kurkod.web.domain.passport.model.request;

import jakarta.persistence.Column;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PassportPutRequest {

    @NotBlank
    @Column(length = 4, nullable = false)
    @Pattern(regexp = "^[0-9]{4}$", message = "Invalid passport series")
    private String series;

    @NotBlank
    @Column(length = 6, nullable = false)
    @Pattern(regexp = "^[0-9]{6}$", message = "Invalid passport number")
    private String number;
}