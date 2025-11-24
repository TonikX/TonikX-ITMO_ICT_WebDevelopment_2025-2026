package io.github.artsobol.kurkod.web.domain.iam.user.service.impl;

import io.github.artsobol.kurkod.web.domain.iam.user.mapper.UserMapper;
import io.github.artsobol.kurkod.web.domain.iam.user.error.UserError;
import io.github.artsobol.kurkod.web.domain.iam.user.model.dto.UserDTO;
import io.github.artsobol.kurkod.web.domain.iam.user.model.entity.User;
import io.github.artsobol.kurkod.common.exception.DataExistException;
import io.github.artsobol.kurkod.common.exception.NotFoundException;
import io.github.artsobol.kurkod.web.domain.iam.user.model.request.UserPatchRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.request.UserPostRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.request.UserPutRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.repository.UserRepository;
import io.github.artsobol.kurkod.web.domain.iam.user.service.api.UserService;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.stream.Collectors;

import static io.github.artsobol.kurkod.common.util.VersionUtils.checkVersion;


@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public UserDTO getById(@NotNull Long userId) {
        return userMapper.toDto(getUserById(userId));
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public List<UserDTO> getAll() {
        return userRepository.findAllByIsActiveTrue().stream().map(userMapper::toDto).toList();
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public UserDTO getByUsername(@NotBlank String username) {
        User response = getUserByUsername(username);
        return userMapper.toDto(response);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public UserDTO create(@NotNull UserPostRequest request) {
        ensureNotExistsByUsername(request.getUsername());
        ensureNotExistsByEmail(request.getEmail());
        User user = userMapper.toEntity(request);
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user = userRepository.save(user);
        return userMapper.toDto(user);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public UserDTO replace(@NotNull Long userId, UserPutRequest request, Long version) {
        User user = getUserById(userId);
        checkVersion(user.getVersion(), version);
        userMapper.updateFully(user, request);
        user = userRepository.save(user);
        return userMapper.toDto(user);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public UserDTO update(@NotNull Long userId, UserPatchRequest request,Long version) {
        User user = getUserById(userId);
        checkVersion(user.getVersion(), version);
        userMapper.updatePartially(user, request);
        user = userRepository.save(user);
        return userMapper.toDto(user);
    }

    @Override
    @Transactional
    @PreAuthorize("hasAnyAuthority('DIRECTOR', 'SUPER_ADMIN')")
    public void deleteById(@NotNull Long userId, Long version) {
        User user = getUserById(userId);
        checkVersion(user.getVersion(), version);
        user.setActive(false);
        userRepository.save(user);
    }

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        return getUserDetails(email, userRepository);
    }

    static UserDetails getUserDetails(String email, UserRepository userRepository) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new NotFoundException(UserError.WITH_EMAIL_ALREADY_EXISTS, email));

        user.setLastLogin(OffsetDateTime.now());
        userRepository.save(user);
        return new org.springframework.security.core.userdetails.User(user.getUsername(),
                user.getPassword(),
                user.getRoles().stream().map(
                        role -> new SimpleGrantedAuthority(role.getName())
                ).collect(Collectors.toList()));
    }

    protected User getUserByUsername(String username) {
        return userRepository.findByUsernameAndIsActiveTrue(username)
                .orElseThrow(() -> new NotFoundException(UserError.NOT_FOUND_BY_USERNAME, username));
    }

    protected User getUserById(Long id) {
        return userRepository.findByIdAndIsActiveTrue(id)
                .orElseThrow(() -> new NotFoundException(UserError.NOT_FOUND_BY_ID, id));
    }

    protected void ensureNotExistsByUsername(String username) {
        if (userRepository.existsByUsername(username)) {
            throw new DataExistException(UserError.WITH_USERNAME_ALREADY_EXISTS, username);
        }
    }

    protected void ensureNotExistsByEmail(String email) {
        if (userRepository.existsByEmail(email)) {
            throw new DataExistException(UserError.WITH_EMAIL_ALREADY_EXISTS, email);
        }
    }
}
