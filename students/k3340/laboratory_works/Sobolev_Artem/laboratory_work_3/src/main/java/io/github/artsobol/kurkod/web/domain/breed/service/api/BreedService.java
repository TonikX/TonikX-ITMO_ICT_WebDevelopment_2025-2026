package io.github.artsobol.kurkod.web.domain.breed.service.api;

import io.github.artsobol.kurkod.web.domain.breed.model.dto.BreedDTO;
import io.github.artsobol.kurkod.web.domain.breed.model.request.BreedPatchRequest;
import io.github.artsobol.kurkod.web.domain.breed.model.request.BreedPostRequest;
import io.github.artsobol.kurkod.web.domain.breed.model.request.BreedPutRequest;

import java.util.List;

public interface BreedService {

    BreedDTO create(BreedPostRequest breedPostRequest);

    BreedDTO get(Long id);

    List<BreedDTO> getAll();

    BreedDTO replace(Long id, BreedPutRequest breedPutRequest, Long version);

    BreedDTO update(Long id, BreedPatchRequest breedPatchRequest, Long version);

    void delete(Long id, Long version);
}
