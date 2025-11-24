package io.github.artsobol.kurkod.web.domain.dismissal.repository;

import io.github.artsobol.kurkod.web.domain.dismissal.model.entity.Dismissal;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface DismissalRepository extends JpaRepository<Dismissal, Long> {

    Optional<Dismissal> findDismissalByWorker_Id(Long id);

    Optional<Dismissal> findDismissalByWorker_IdAndWhoDismiss_Id(Long workerId, Long whoDismissedId);

    List<Dismissal> findAllByWorker_Id(Long id);

    List<Dismissal> findAllByWhoDismiss_Id(Long id);

    boolean existsByWorker_IdAndWhoDismiss_Id(Long workerId, Long whoDismissedId);
}
