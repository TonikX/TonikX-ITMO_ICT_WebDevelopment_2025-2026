package io.github.artsobol.kurkod.web.domain.staff.repository;

import io.github.artsobol.kurkod.web.domain.staff.model.entity.Staff;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface StaffRepository extends JpaRepository<Staff, Long> {

    Optional<Staff> findStaffByIdAndIsActiveTrue(Long id);

    List<Staff> findAllByIsActiveTrue();
}
