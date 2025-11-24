package io.github.artsobol.kurkod.web.domain.eggproductionmonth.mapper;

import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.dto.EggProductionMonthDTO;
import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.entity.EggProductionMonth;
import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.request.EggProductionMonthPatchRequest;
import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.request.EggProductionMonthPostRequest;
import io.github.artsobol.kurkod.web.domain.eggproductionmonth.model.request.EggProductionMonthPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface EggProductionMonthMapper {

    @Mapping(target = "chickenId", source = "chicken.id")
    EggProductionMonthDTO toDto(EggProductionMonth eggProductionMonth);

    EggProductionMonth toEntity(EggProductionMonthPostRequest eggProductionMonthPostRequest);

    void replace(@MappingTarget EggProductionMonth eggProductionMonth, EggProductionMonthPutRequest eggProductionMonthPutRequest);

    void update(@MappingTarget EggProductionMonth eggProductionMonth, EggProductionMonthPatchRequest eggProductionMonthPatchRequest);


}
