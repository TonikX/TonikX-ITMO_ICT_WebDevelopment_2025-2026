package io.github.artsobol.kurkod.web.domain.employmentcontract.mapper;

import io.github.artsobol.kurkod.web.domain.employmentcontract.model.dto.EmploymentContractDTO;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.entity.EmploymentContract;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.request.EmploymentContractPatchRequest;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.request.EmploymentContractPostRequest;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.request.EmploymentContractPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface EmploymentContractMapper {

    @Mapping(target = "position", source = "staff.position")
    @Mapping(target = "firstNameWorker", source = "worker.firstName")
    @Mapping(target = "lastNameWorker", source = "worker.lastName")
    EmploymentContractDTO toDto(EmploymentContract employmentContract);

    @Mapping(target = "staff", ignore = true)
    EmploymentContract toEntity(EmploymentContractPostRequest employmentContractPostRequest);

    @Mapping(target = "staff", ignore = true)
    void updateFully(@MappingTarget EmploymentContract employmentContract, EmploymentContractPutRequest employmentContractPutRequest);

    @Mapping(target = "staff", ignore = true)
    void updatePartially(@MappingTarget EmploymentContract employmentContract, EmploymentContractPatchRequest employmentContractPatchRequest);
}
