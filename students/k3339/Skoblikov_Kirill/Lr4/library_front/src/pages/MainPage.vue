<template>
  <div class="main">
    <div class="center-wrapper">
      <h1>Добро пожаловать в систему управления библиотекой!</h1>
      <my-button
        class="btn"
        @click="GoToRegister"
      >
        Зарегистрироваться
      </my-button>
      <my-button
        class="btn"
        @click="GoToLogin"
      >
        Авторизоваться
      </my-button>
      </div>
  </div>
</template>

<script>
import MyButton from "@/components/UI/MyButton.vue";
export default {
  components: {
    MyButton
  },
  methods: {
    GoToRegister() {
      this.$router.push('/register');
    },
    GoToLogin() {
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.main {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.center-wrapper {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 20px;
}

h1 {
  color: white;
  font-size: 2.5rem;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}
</style>