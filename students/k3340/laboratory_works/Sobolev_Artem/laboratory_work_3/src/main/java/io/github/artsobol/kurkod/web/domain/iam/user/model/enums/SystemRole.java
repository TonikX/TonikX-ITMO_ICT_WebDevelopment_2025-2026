package io.github.artsobol.kurkod.web.domain.iam.user.model.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum SystemRole {
    USER("USER", 1, "Работник фабрики"),
    DIRECTOR("DIRECTOR", 2, "Директор птицефабрики"),
    ADMIN("ADMIN", 3, "Системный администратор"),
    SUPER_ADMIN("SUPER_ADMIN", 4, "Главный администратор")
    ;

    private final String role;
    private final int accessLevel;
    private final String description;

    public static SystemRole fromString(String role) {
        return SystemRole.valueOf(role.toUpperCase());
    }
}
