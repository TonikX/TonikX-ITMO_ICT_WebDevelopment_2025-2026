package io.github.artsobol.kurkod.web.domain.chicken.mapper;

import io.github.artsobol.kurkod.web.domain.chicken.model.dto.ChickenDTO;
import io.github.artsobol.kurkod.web.domain.chicken.model.entity.Chicken;
import io.github.artsobol.kurkod.web.domain.chicken.model.request.ChickenPatchRequest;
import io.github.artsobol.kurkod.web.domain.chicken.model.request.ChickenPostRequest;
import io.github.artsobol.kurkod.web.domain.chicken.model.request.ChickenPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.NullValuePropertyMappingStrategy;

@Mapper(componentModel = "spring",
nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
public interface ChickenMapper {

    @Mapping(source = "cage.id", target = "cageId")
    @Mapping(source = "breed.id", target = "breedId")
    ChickenDTO toDto(Chicken chicken);

    Chicken toEntity(ChickenPostRequest chickenPostRequest);

    @Mapping(target = "cage", ignore = true)
    @Mapping(target = "breed", ignore = true)
    void updateFully(@MappingTarget Chicken chicken, ChickenPutRequest chickenPutRequest);

    @Mapping(target = "cage", ignore = true)
    @Mapping(target = "breed", ignore = true)
    void updatePartially(@MappingTarget Chicken chicken, ChickenPatchRequest chickenPatchRequest);
}
