package io.github.artsobol.kurkod.web.domain.breed.service.impl;

import io.github.artsobol.kurkod.common.exception.NotFoundException;
import io.github.artsobol.kurkod.web.domain.breed.error.BreedError;
import io.github.artsobol.kurkod.web.domain.breed.model.entity.Breed;
import io.github.artsobol.kurkod.web.domain.breed.repository.BreedRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class BreedLookupService {

    private final BreedRepository breedRepository;

    public Breed getBreedByIdOrThrow(Long id) {
        return breedRepository.findBreedByIdAndIsActiveTrue(id)
                .orElseThrow(() -> new NotFoundException(BreedError.NOT_FOUND_BY_ID, id));
    }
}
