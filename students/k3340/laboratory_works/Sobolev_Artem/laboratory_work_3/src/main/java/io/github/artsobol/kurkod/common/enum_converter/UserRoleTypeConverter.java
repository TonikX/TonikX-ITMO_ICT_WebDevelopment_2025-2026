package io.github.artsobol.kurkod.common.enum_converter;

import io.github.artsobol.kurkod.web.domain.iam.user.model.enums.SystemRole;
import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;

@Converter
public class UserRoleTypeConverter implements AttributeConverter<SystemRole, String> {
    @Override
    public String convertToDatabaseColumn(SystemRole userRole) {
        return userRole.name();
    }

    @Override
    public SystemRole convertToEntityAttribute(String s) {
        return SystemRole.fromString(s);
    }
}
