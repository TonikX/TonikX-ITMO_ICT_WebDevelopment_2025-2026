package io.github.artsobol.kurkod.web.domain.rows.mapper;

import io.github.artsobol.kurkod.web.domain.rows.model.dto.RowsDTO;
import io.github.artsobol.kurkod.web.domain.rows.model.entity.Rows;
import io.github.artsobol.kurkod.web.domain.rows.model.request.RowsPatchRequest;
import io.github.artsobol.kurkod.web.domain.rows.model.request.RowsPostRequest;
import io.github.artsobol.kurkod.web.domain.rows.model.request.RowsPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface RowsMapper {

    @Mapping(target = "workshopId", source = "workshop.id")
    RowsDTO toDto(Rows rows);

    @Mapping(target = "workshop", ignore = true)
    Rows toEntity(RowsPostRequest rowsPostRequest);

    @Mapping(target = "workshop", ignore = true)
    void update(@MappingTarget Rows rows, RowsPatchRequest rowsPatchRequest);

    @Mapping(target = "workshop", ignore = true)
    void replace(@MappingTarget Rows rows, RowsPutRequest rowsPutRequest);
}
