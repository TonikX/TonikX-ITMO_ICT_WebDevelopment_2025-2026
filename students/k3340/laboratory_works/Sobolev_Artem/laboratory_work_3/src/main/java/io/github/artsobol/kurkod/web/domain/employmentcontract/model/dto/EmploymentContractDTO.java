package io.github.artsobol.kurkod.web.domain.employmentcontract.model.dto;


import java.time.LocalDate;
import java.time.OffsetDateTime;

public record EmploymentContractDTO(
        String contractNumber,
        Integer salary,
        String position,
        String firstNameWorker,
        String lastNameWorker,
        LocalDate startDate,
        LocalDate endDate,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt,
        Long version
) {
};
