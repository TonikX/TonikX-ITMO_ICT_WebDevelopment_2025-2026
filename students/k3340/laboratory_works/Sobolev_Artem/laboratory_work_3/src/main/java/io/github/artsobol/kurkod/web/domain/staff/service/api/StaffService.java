package io.github.artsobol.kurkod.web.domain.staff.service.api;

import io.github.artsobol.kurkod.web.domain.staff.model.dto.StaffDTO;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPatchRequest;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPostRequest;
import io.github.artsobol.kurkod.web.domain.staff.model.request.StaffPutRequest;

import java.util.List;

public interface StaffService {

    StaffDTO get(Long id);

    List<StaffDTO> getAll();

    StaffDTO create(StaffPostRequest request);

    StaffDTO replace(Long id, StaffPutRequest request, Long version);

    StaffDTO update(Long id, StaffPatchRequest request, Long version);

    void delete(Long id, Long version);
}
