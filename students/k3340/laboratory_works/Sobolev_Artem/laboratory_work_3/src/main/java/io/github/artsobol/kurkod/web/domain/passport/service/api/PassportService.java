package io.github.artsobol.kurkod.web.domain.passport.service.api;

import io.github.artsobol.kurkod.web.domain.passport.model.dto.PassportDTO;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPostRequest;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPutRequest;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPatchRequest;

public interface PassportService {

    PassportDTO get(Long workerId);

    PassportDTO create(Long workerId, PassportPostRequest request);

    PassportDTO replace(Long workerId, PassportPutRequest request, Long version);

    PassportDTO update(Long workerId, PassportPatchRequest request, Long version);

    void delete(Long workerId, Long version);
}
