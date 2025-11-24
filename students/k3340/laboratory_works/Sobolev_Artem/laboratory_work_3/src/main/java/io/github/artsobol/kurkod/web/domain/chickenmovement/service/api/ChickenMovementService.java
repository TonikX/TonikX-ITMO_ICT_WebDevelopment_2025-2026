package io.github.artsobol.kurkod.web.domain.chickenmovement.service.api;

import io.github.artsobol.kurkod.web.domain.chickenmovement.model.dto.ChickenMovementDTO;
import io.github.artsobol.kurkod.web.domain.chickenmovement.model.entity.ChickenMovement;
import io.github.artsobol.kurkod.web.domain.chickenmovement.model.request.ChickenMovementPostRequest;

import java.time.LocalDateTime;
import java.util.List;

public interface ChickenMovementService {

    ChickenMovementDTO get(Long movementId);

    ChickenMovementDTO getCurrentCage(Long chickenId);

    List<ChickenMovementDTO> getAllByChickenId(Long chickenId);

    ChickenMovementDTO create(Long chickenId, ChickenMovementPostRequest request);
}
