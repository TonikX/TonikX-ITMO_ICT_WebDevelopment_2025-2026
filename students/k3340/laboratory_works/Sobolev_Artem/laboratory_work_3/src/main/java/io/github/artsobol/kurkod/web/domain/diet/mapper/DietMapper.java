package io.github.artsobol.kurkod.web.domain.diet.mapper;

import io.github.artsobol.kurkod.web.domain.diet.model.dto.DietDTO;
import io.github.artsobol.kurkod.web.domain.diet.model.entity.Diet;
import io.github.artsobol.kurkod.web.domain.diet.model.request.DietPatchRequest;
import io.github.artsobol.kurkod.web.domain.diet.model.request.DietPostRequest;
import io.github.artsobol.kurkod.web.domain.diet.model.request.DietPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface DietMapper {

    DietDTO toDTO(Diet diet);

    @Mapping(target = "breeds", ignore = true)
    Diet toEntity(DietPostRequest dietPostRequest);

    @Mapping(target = "breeds", ignore = true)
    void update(@MappingTarget Diet diet, DietPatchRequest dietPatchRequest);

    @Mapping(target = "breeds", ignore = true)
    void replace(@MappingTarget Diet diet, DietPutRequest dietPutRequest);
}
