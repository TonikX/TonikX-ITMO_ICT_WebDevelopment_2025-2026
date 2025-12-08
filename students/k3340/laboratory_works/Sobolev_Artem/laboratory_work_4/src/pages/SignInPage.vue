<template>
  <div class="sign-in">
    <div class="sign-in__window">
      <div class="sign-in__window__first-column">
        <Logo :custom-style="true"/>
        <p class="sign-in__description-first">
          Для входа зарегистрируйтесь
        </p>
        <Button
            label="Регистрация"
            mode="white-no-switch"
            location="sign-in-button"
            style="width: 262px;"
            @click="goToRegister"
        />
        <p class="sign-in__copyright">
          © 2025 КурКод
        </p>
      </div>

      <div class="sign-in__window__second-column">
        <div class="sign-in__window__buttons">
          <Button
              class="header__nav-link"
              @click="ui.toggleTheme"
              :icon-name="ui.theme === 'light' ? 'light' : 'dark'"
          />
        </div>

        <h2 class="sign-in__title">
          Авторизация
        </h2>
        <p class="sign-in__text" style="padding-bottom: 10px;">
          Для входа в систему укажите корпоративную почту и пароль.
        </p>

        <form @submit.prevent="login" class="sign-in__form">
          <input
              class="sign-in__input"
              type="email"
              v-model="email"
              placeholder="Почта"
              required
          />
          <input
              class="sign-in__input"
              type="password"
              v-model="password"
              placeholder="Пароль"
              required
          />

          <p v-if="errorMessage" style="color:#ff4d4f; font-weight:600">{{ errorMessage }}</p>
          <p v-if="successMessage" style="color:#4caf50; font-weight:600">{{ successMessage }}</p>

          <Button
              :disabled="loading"
              label="Войти"
              mode="violet-no-switch"
              type="submit"
              location="sign-in-button"
              style="width: 339px;"
          />
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import Logo from "@/components/ui/Logo.vue";
import Button from "@/components/ui/Button.vue";
import {uiStore} from "@/stores/ui.js";
import {loginUser} from "@/api/auth.js";

const ui = uiStore();

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const loading = ref(false);

const login = async () => {
  errorMessage.value = "";
  successMessage.value = "";
  loading.value = true;

  try {
    const res = await loginUser({email: email.value, password: password.value});
    console.log("LOGIN RESPONSE:", res);

    localStorage.setItem("refreshToken", res.refreshToken);
    ui.accessToken = res.token;

    successMessage.value = "Успешный вход!";
    setTimeout(() => window.location.href = "/", 500);
  } catch (err) {
    console.log("ERROR:", err);
    errorMessage.value = err.response?.data?.message || "Ошибка авторизации";
  }
};

const goToRegister = () => {
  window.location.href = "/register";
};
</script>

<style lang="scss" scoped>
.sign-in {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 85vh;

  &__window {
    width: 1100px;
    height: 514px;
    border-radius: 16px;
    overflow: hidden;
    background: var(--section-bg);
    display: grid;
    grid-template-columns: 332px 768px;

    &__first-column {
      background-color: var(--color-section-contrast-light);
      color: var(--color-white);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding-top: 56px;
      padding-bottom: 24px;
      padding-inline: 35px;
    }

    &__second-column {
      display: flex;
      flex-direction: column;
      justify-content: start;
      align-items: center;
      padding-top: 18px;
      padding-right: 24px;

      background-image: url('/images/sign-in-bg.svg');
      background-repeat: no-repeat;
      background-size: 109px 370px;
      background-position: calc(0% + 24px) calc(100% - 35px);
    }

    &__buttons {
      display: flex;
      flex-direction: row;
      justify-content: flex-end;
      align-self: flex-end;
      gap: 24px;
    }
  }

  &__description-first {
    font-weight: 600;
    font-size: 20px;
    line-height: 200%;
    text-align: center;
    max-width: 262px;
    padding-top: 49px;
    padding-bottom: 48px;
  }

  &__copyright {
    font-weight: 400;
    font-size: 14px;
    color: #fff;
    text-align: left;
    align-self: flex-start;
    padding-top: 51px;
  }

  &__title {
    font-weight: 700;
    font-size: 24px;
    padding-bottom: 30px;
  }

  &__text {
    font-weight: 500;
    font-size: 14px;
    color: var(--color);
  }

  &__form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 16px;
    padding-block: 16px;
  }

  &__input {
    border-radius: 8px;
    width: 339px;
    height: 48px;
    background: var(--color-bg-light);
    color: var(--color-text-light);
    display: flex;
    flex-direction: row;
    align-items: center;
    padding-inline: 24px;
  }

  &__select {
    width: 168px;
    height: 32px;
    font-weight: 500;
    font-size: 14px;
    color: #686590;
    border-radius: 8px;
    outline: none;
    padding-left: 12px;
    background: var(--color-bg-light);
    appearance: none;
    background-image: url('@/assets/icons/select-arrow.svg');
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 12px;
  }

  &__select__option {
    font-weight: 500;
    font-size: 14px;
    color: var(--color-text-light);
    width: 168px;
    outline: none;
  }
}

</style>