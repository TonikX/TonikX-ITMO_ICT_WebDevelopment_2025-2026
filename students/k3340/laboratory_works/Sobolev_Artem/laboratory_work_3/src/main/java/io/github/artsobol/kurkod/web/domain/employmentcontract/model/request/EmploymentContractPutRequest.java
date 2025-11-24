package io.github.artsobol.kurkod.web.domain.employmentcontract.model.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class EmploymentContractPutRequest {

    @NotBlank
    @Size(min = 2, max = 20, message = "Contract number should be between 2 and 20 characters")
    private String contractNumber;

    @NotNull
    @Positive
    private Integer salary;

    @NotNull
    private Long staffId;

    @NotNull
    private LocalDate startDate;

    @NotNull
    private LocalDate endDate;
}
