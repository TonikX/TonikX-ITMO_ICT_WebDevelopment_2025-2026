package io.github.artsobol.kurkod.web.domain.dismissal.service.api;

import io.github.artsobol.kurkod.web.domain.dismissal.model.dto.DismissalDTO;
import io.github.artsobol.kurkod.web.domain.dismissal.model.request.DismissalPostRequest;
import io.github.artsobol.kurkod.web.domain.dismissal.model.request.DismissalPutRequest;
import io.github.artsobol.kurkod.web.domain.dismissal.model.request.DismissalPatchRequest;

import java.util.List;

public interface DismissalService {

    DismissalDTO getByWorkerAndDismissed(Long workerId, Long dismissedId);

    List<DismissalDTO> getAllByWorker(Long workerId);

    List<DismissalDTO> getAllByDismissed(Long dismissedId);

    DismissalDTO create(DismissalPostRequest request);

    DismissalDTO replace(Long workerId, DismissalPutRequest request, Long version);

    DismissalDTO update(Long workerId, DismissalPatchRequest request, Long version);
}
