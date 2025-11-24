package io.github.artsobol.kurkod.web.domain.chicken.service.api;

import io.github.artsobol.kurkod.web.domain.chicken.model.dto.ChickenDTO;
import io.github.artsobol.kurkod.web.domain.chicken.model.request.ChickenPatchRequest;
import io.github.artsobol.kurkod.web.domain.chicken.model.request.ChickenPutRequest;
import io.github.artsobol.kurkod.web.domain.chicken.model.request.ChickenPostRequest;

import java.util.List;

public interface ChickenService {

    ChickenDTO create(ChickenPostRequest request);

    ChickenDTO get(Long id);

    List<ChickenDTO> getAll();

    void delete(Long id, Long version);

    ChickenDTO replace(Long id, ChickenPutRequest request, Long version);

    ChickenDTO update(Long id, ChickenPatchRequest request, Long version);
}
