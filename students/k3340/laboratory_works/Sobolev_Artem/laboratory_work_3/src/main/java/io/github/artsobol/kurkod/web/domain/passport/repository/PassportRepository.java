package io.github.artsobol.kurkod.web.domain.passport.repository;

import io.github.artsobol.kurkod.web.domain.passport.model.entity.Passport;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface PassportRepository extends JpaRepository<Passport, Long> {

    Optional<Passport> findPassportByWorkerIdAndIsActiveTrue(Long workerId);

    void deletePassportByWorkerId(Long workerId);
}
