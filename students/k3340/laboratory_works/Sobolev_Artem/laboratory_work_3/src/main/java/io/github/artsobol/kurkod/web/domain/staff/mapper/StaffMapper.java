package io.github.artsobol.kurkod.web.domain.staff.mapper;

import io.github.artsobol.kurkod.web.domain.staff.model.dto.StaffDTO;
import io.github.artsobol.kurkod.web.domain.staff.model.entity.Staff;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPatchRequest;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPostRequest;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring",
nullValuePropertyMappingStrategy = org.mapstruct.NullValuePropertyMappingStrategy.IGNORE)
public interface StaffMapper {

    StaffDTO toDto(Staff staff);

    Staff toEntity(StaffPostRequest staffPostRequest);

    void updateFully(@MappingTarget Staff staff, StaffPutRequest staffPutRequest);

    void updatePartially(@MappingTarget Staff staff, StaffPatchRequest staffPatchRequest);
}
