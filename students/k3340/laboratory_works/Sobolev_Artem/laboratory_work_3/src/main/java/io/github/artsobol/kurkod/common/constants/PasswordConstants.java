package io.github.artsobol.kurkod.common.constants;

import lombok.NoArgsConstructor;

@NoArgsConstructor(access = lombok.AccessLevel.PRIVATE)
public class PasswordConstants {
    public static final String PASSWORD_ALL_CHARACTERS =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~`!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?";
    public static final String PASSWORD_LETTERS_UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    public static final String PASSWORD_LETTERS_LOWER_CASE = "abcdefghijklmnopqrstuvwxyz";
    public static final String PASSWORD_DIGITS = "0123456789";
    public static final String PASSWORD_CHARACTERS = "~`!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?";
    public static final Integer REQUIRED_MIN_PASSWORD_LENGTH = 8;
    public static final Integer REQUIRED_MIN_LETTERS_NUMBER_EVERY_CASE_IN_PASSWORD = 1;
    public static final Integer REQUIRED_MIN_DIGITS_NUMBER_IN_PASSWORD = 1;
    public static final Integer REQUIRED_MIN_CHARACTERS_NUMBER_IN_PASSWORD = 1;
}