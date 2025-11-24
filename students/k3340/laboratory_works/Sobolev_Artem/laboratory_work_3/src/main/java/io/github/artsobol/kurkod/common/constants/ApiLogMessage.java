package io.github.artsobol.kurkod.common.constants;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum ApiLogMessage {
    NAME_OF_CURRENT_METHOD("Current method: {}"),
    CREATE_ENTITY("User '{}' created {} entity: id={}"),
    REPLACE_ENTITY("User '{}' replaced {} entity: id={}"),
    UPDATE_ENTITY("User '{}' updated {} entity: id={}"),
    DELETE_ENTITY("User '{}' deleted {} entity: id={}"),
    GET_ENTITY("User '{}' retrieved {} entity: id={}"),
    GET_ALL_ENTITIES("User '{}' retrieved all {} entities"),
    ;

    private final String value;
}
