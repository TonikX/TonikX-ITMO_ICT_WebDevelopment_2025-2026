package io.github.artsobol.kurkod.web.domain.dismissal.model.dto;

import java.time.LocalDate;

public record DismissalDTO(
        Integer id, LocalDate dismissalDate, String reason, String worker, String whoDismiss, Long version
) {
};