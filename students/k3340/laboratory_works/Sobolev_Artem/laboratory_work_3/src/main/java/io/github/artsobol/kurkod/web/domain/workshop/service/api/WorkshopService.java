package io.github.artsobol.kurkod.web.domain.workshop.service.api;

import io.github.artsobol.kurkod.web.domain.workshop.model.dto.WorkshopDTO;
import io.github.artsobol.kurkod.web.domain.workshop.model.request.WorkshopPatchRequest;
import io.github.artsobol.kurkod.web.domain.workshop.model.request.WorkshopPostRequest;
import io.github.artsobol.kurkod.web.domain.workshop.model.request.WorkshopPutRequest;

import java.util.List;

public interface WorkshopService {

    WorkshopDTO get(Long id);

    List<WorkshopDTO> getAll();

    WorkshopDTO create(WorkshopPostRequest request);

    WorkshopDTO update(Long id, WorkshopPatchRequest request, Long version);

    WorkshopDTO replace(Long id, WorkshopPutRequest request, Long version);

    void delete(Long id, Long version);
}
