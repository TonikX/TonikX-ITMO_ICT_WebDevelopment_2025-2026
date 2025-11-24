package io.github.artsobol.kurkod.web.domain.iam.userrole.model.entity;

import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name = "user_role")
public class UserRole extends BaseEntity {

    private String title;
}
