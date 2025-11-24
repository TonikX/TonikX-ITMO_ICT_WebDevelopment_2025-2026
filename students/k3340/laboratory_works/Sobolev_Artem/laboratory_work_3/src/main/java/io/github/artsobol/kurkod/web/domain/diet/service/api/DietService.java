package io.github.artsobol.kurkod.web.domain.diet.service.api;

import io.github.artsobol.kurkod.web.domain.diet.model.dto.DietDTO;
import io.github.artsobol.kurkod.web.domain.diet.model.request.DietPatchRequest;
import io.github.artsobol.kurkod.web.domain.diet.model.request.DietPostRequest;
import io.github.artsobol.kurkod.web.domain.diet.model.request.DietPutRequest;

import java.util.List;

public interface DietService {

    DietDTO get(Long id);

    List<DietDTO> getAll();

    DietDTO create(DietPostRequest request);

    DietDTO update(Long id, DietPatchRequest request, Long version);

    DietDTO replace(Long id, DietPutRequest request, Long version);

    void delete(Long id, Long expectedVersion);
}
