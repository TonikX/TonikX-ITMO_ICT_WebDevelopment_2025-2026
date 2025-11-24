package io.github.artsobol.kurkod.web.domain.iam.user.model.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class UserPutRequest {

    @NotBlank
    @Size(max = 30, message = "Username should be less than 30 characters")
    private String username;

    @NotNull
    @Size(max = 255)
    private String password;

    @Email
    @NotNull
    @Size(max = 80)
    private String email;
}
