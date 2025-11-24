package io.github.artsobol.kurkod.web.domain.eggproductionmonth.error;


import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum EggProductionMonthError implements ErrorDescriptor {
    NOT_FOUND_BY_KEYS("EPM-404", "egg_production_month.not_found_by_keys", HttpStatus.NOT_FOUND),
    ALREADY_EXISTS("EPM-409", "egg_production_month.already_exists", HttpStatus.CONFLICT),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}

