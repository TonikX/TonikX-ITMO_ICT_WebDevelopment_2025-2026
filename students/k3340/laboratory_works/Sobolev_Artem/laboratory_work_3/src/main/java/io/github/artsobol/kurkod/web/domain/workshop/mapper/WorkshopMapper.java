package io.github.artsobol.kurkod.web.domain.workshop.mapper;

import io.github.artsobol.kurkod.web.domain.workshop.model.dto.WorkshopDTO;
import io.github.artsobol.kurkod.web.domain.workshop.model.entity.Workshop;
import io.github.artsobol.kurkod.web.domain.workshop.model.request.WorkshopPatchRequest;
import io.github.artsobol.kurkod.web.domain.workshop.model.request.WorkshopPostRequest;
import io.github.artsobol.kurkod.web.domain.workshop.model.request.WorkshopPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface WorkshopMapper {

    WorkshopDTO toDto(Workshop workshop);

    Workshop toEntity(WorkshopPostRequest workshopPostRequest);

    void replace(@MappingTarget Workshop workshop, WorkshopPutRequest workshopPutRequest);

    void update(@MappingTarget Workshop workshop, WorkshopPatchRequest workshopPatchRequest);
}
