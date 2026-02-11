<template>
  <v-container class="justify-center d-flex">
    <v-card width="500" class="pa-6">
      <h2 class="text-h5 mb-4 d-flex align-center">
        <v-icon icon="mdi-account-cog" color="primary" class="mr-3"></v-icon>
        Настройки профиля
      </h2>
      
      <v-divider class="mb-6"></v-divider>
      
      <h3 class="text-subtitle-1 mb-4 font-weight-bold">Смена пароля</h3>
      
      <v-text-field 
        v-model="currentPassword" 
        label="Текущий пароль" 
        type="password"
        variant="outlined"
        prepend-inner-icon="mdi-lock-outline"
      ></v-text-field>

      <v-text-field 
        v-model="newPassword" 
        label="Новый пароль" 
        type="password"
        variant="outlined"
        prepend-inner-icon="mdi-lock-plus"
      ></v-text-field>
      
      <v-btn color="primary" block size="large" @click="changePassword" :disabled="!currentPassword || !newPassword">
        Сохранить изменения
      </v-btn>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';
export default {
  data: () => ({ currentPassword: '', newPassword: '' }),
  methods: {
    async changePassword() {
      const token = localStorage.getItem('auth_token');
      try {
        await axios.post('http://127.0.0.1:8000/auth/users/set_password/', 
          { 
            new_password: this.newPassword, 
            re_new_password: this.newPassword,
            current_password: this.currentPassword 
          }, 
          { headers: { Authorization: `Token ${token}` } }
        );
        alert('Пароль успешно изменен!');
        this.currentPassword = '';
        this.newPassword = '';
      } catch (e) {
        alert('Ошибка! Проверьте текущий пароль.');
      }
    }
  }
}
</script>