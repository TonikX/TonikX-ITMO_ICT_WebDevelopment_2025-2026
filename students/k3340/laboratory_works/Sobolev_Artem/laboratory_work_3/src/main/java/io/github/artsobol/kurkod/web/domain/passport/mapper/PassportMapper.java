package io.github.artsobol.kurkod.web.domain.passport.mapper;

import io.github.artsobol.kurkod.web.domain.passport.model.dto.PassportDTO;
import io.github.artsobol.kurkod.web.domain.passport.model.entity.Passport;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPatchRequest;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPostRequest;
import io.github.artsobol.kurkod.web.domain.passport.model.request.PassportPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface PassportMapper {

    PassportDTO toDto(Passport passport);

    Passport toEntity(PassportPostRequest passportPostRequest);

    void updateFully(@MappingTarget Passport passport, PassportPutRequest passportPutRequest);

    void updatePartially(@MappingTarget Passport passport, PassportPatchRequest passportPatchRequest);
}
