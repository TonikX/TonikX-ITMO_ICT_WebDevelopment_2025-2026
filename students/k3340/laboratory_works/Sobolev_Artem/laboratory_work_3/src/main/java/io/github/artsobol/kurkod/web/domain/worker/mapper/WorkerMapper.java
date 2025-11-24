package io.github.artsobol.kurkod.web.domain.worker.mapper;

import io.github.artsobol.kurkod.web.domain.worker.model.dto.WorkerDTO;
import io.github.artsobol.kurkod.web.domain.worker.model.entity.Worker;
import io.github.artsobol.kurkod.web.domain.worker.model.request.WorkerPatchRequest;
import io.github.artsobol.kurkod.web.domain.worker.model.request.WorkerPostRequest;
import io.github.artsobol.kurkod.web.domain.worker.model.request.WorkerPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring",
nullValuePropertyMappingStrategy = org.mapstruct.NullValuePropertyMappingStrategy.IGNORE)
public interface WorkerMapper {

    WorkerDTO toDto(Worker worker);

    Worker toEntity(WorkerPostRequest workerPostRequest);

    void updateFully(@MappingTarget Worker worker, WorkerPutRequest workerPutRequest);

    void updatePartially(@MappingTarget Worker worker, WorkerPatchRequest workerPatchRequest);
}
