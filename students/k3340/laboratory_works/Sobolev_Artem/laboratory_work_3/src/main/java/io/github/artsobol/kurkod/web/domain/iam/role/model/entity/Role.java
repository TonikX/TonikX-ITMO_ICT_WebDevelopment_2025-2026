package io.github.artsobol.kurkod.web.domain.iam.role.model.entity;

import io.github.artsobol.kurkod.web.domain.common.BaseEntity;
import io.github.artsobol.kurkod.web.domain.iam.user.model.enums.SystemRole;
import io.github.artsobol.kurkod.common.enum_converter.UserRoleTypeConverter;
import io.github.artsobol.kurkod.web.domain.iam.user.model.entity.User;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.HashSet;
import java.util.Set;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name = "role")
public class Role extends BaseEntity {
    @Column(nullable = false)
    private String name;

    @Column(name = "user_system_role", nullable = false, updatable = false)
    @Convert(converter = UserRoleTypeConverter.class)
    private SystemRole userSystemRole;

    @ManyToMany(fetch = FetchType.LAZY, mappedBy = "roles", cascade = CascadeType.MERGE)
    private Set<User> users = new HashSet<>();
}
