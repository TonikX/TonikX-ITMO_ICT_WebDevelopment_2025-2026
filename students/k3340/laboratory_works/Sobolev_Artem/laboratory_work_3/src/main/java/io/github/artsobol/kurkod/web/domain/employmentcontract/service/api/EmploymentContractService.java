package io.github.artsobol.kurkod.web.domain.employmentcontract.service.api;

import io.github.artsobol.kurkod.web.domain.employmentcontract.model.dto.EmploymentContractDTO;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.request.EmploymentContractPatchRequest;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.request.EmploymentContractPostRequest;
import io.github.artsobol.kurkod.web.domain.employmentcontract.model.request.EmploymentContractPutRequest;

public interface EmploymentContractService {

    EmploymentContractDTO get(Long workerId);

    EmploymentContractDTO create(Long workerId, EmploymentContractPostRequest request);

    EmploymentContractDTO replace(Long workerId, EmploymentContractPutRequest request, Long expectedVersion);

    EmploymentContractDTO update(Long workerId, EmploymentContractPatchRequest request, Long expectedVersion);

    void delete(Long workerId, Long expectedVersion);
}
