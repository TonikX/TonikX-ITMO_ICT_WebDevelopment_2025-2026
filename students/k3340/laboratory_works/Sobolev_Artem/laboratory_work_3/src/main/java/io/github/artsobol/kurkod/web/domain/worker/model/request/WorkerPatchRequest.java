package io.github.artsobol.kurkod.web.domain.worker.model.request;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class WorkerPatchRequest {

    private String firstName;

    private String lastName;

    private String patronymic;
}
