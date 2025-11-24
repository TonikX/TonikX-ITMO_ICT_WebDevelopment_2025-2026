package io.github.artsobol.kurkod.web.domain.cage.service.api;

import io.github.artsobol.kurkod.web.domain.cage.model.dto.CageDTO;
import io.github.artsobol.kurkod.web.domain.cage.model.request.CagePatchRequest;
import io.github.artsobol.kurkod.web.domain.cage.model.request.CagePostRequest;
import io.github.artsobol.kurkod.web.domain.cage.model.request.CagePutRequest;

import java.util.List;

public interface CageService {

    CageDTO find(Long rowId, Integer cageNumber);

    List<CageDTO> findAll(Long rowId);

    CageDTO create(Long rowId, CagePostRequest request);

    CageDTO replace(Long rowId, Integer cageNumber, CagePutRequest request, Long expectedVersion);

    CageDTO update(Long rowId, Integer cageNumber, CagePatchRequest request, Long expectedVersion);

    void delete(Long rowId, Integer cageNumber, Long expectedVersion);
}
