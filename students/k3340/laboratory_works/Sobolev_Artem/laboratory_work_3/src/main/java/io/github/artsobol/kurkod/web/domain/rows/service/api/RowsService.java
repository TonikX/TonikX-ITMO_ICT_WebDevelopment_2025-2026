package io.github.artsobol.kurkod.web.domain.rows.service.api;

import io.github.artsobol.kurkod.web.domain.rows.model.dto.RowsDTO;
import io.github.artsobol.kurkod.web.domain.rows.model.request.RowsPatchRequest;
import io.github.artsobol.kurkod.web.domain.rows.model.request.RowsPostRequest;
import io.github.artsobol.kurkod.web.domain.rows.model.request.RowsPutRequest;

import java.util.List;

public interface RowsService {

    RowsDTO find(Long workshopId, Integer rowHumber);

    List<RowsDTO> findAll(Long workshopId);

    RowsDTO create(Long workshopId, RowsPostRequest request);

    RowsDTO update(Long workshopId, Integer rowHumber, RowsPatchRequest request, Long version);

    RowsDTO replace(Long workshopId, Integer rowHumber, RowsPutRequest request, Long version);

    void delete(Long workshopId, Integer rowHumber, Long version);
}
