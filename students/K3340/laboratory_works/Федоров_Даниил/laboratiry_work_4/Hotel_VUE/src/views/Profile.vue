<template>
  <v-container>
    <h2>Профиль</h2>

    <v-card class="pa-4 mb-6">
      <h3>Ваши данные</h3>
      <v-text-field label="Логин" v-model="profileData.username" :readonly="!editMode" :variant="editMode ? 'outlined' : 'plain'" />
      <v-text-field label="Email" v-model="profileData.email" :readonly="!editMode" :variant="editMode ? 'outlined' : 'plain'" />
      <v-card-actions>
        <v-btn v-if="!editMode" color="primary" @click="editMode = true">Редактировать</v-btn>
        <div v-else>
          <v-btn color="success" @click="updateProfile" class="mr-2">Сохранить</v-btn>
          <v-btn color="grey" @click="editMode = false">Отмена</v-btn>
        </div>
      </v-card-actions>
    </v-card>

    <v-card class="pa-4">
      <h3>Смена пароля</h3>
      <v-card-text>
        <v-text-field label="Текущий пароль" type="password" v-model="profilePassword.current_password" />
        <v-text-field label="Новый пароль" type="password" v-model="profilePassword.new_password" />
      </v-card-text>
      <v-card-actions>
        <v-btn color="error" @click="updatePassword">Сменить пароль</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { useTokenStore } from '@/stores/token';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const token = useTokenStore();
const editMode = ref(false);

const profileData = ref({
  username: '',
  email: '',
});

const profilePassword = ref({
  new_password: '',
  current_password: '',
});

const profile = async () => {
  try {
    const res = await axios.get('api/auth/users/me/', {
      headers: { Authorization: `Token ${token.token}` },
    });
    profileData.value.username = res.data.username;
    profileData.value.email = res.data.email;
  } catch (error) {
    console.error('Ошибка получения данных', error);
  }
};

const updateProfile = async () => {
  try {
    await axios.patch(
      'api/auth/users/me/',
      {
        username: profileData.value.username,
        email: profileData.value.email,
      },
      {
        headers: { Authorization: `Token ${token.token}` },
      }
    );
    await profile();
    alert('Профиль успешно обновлён');
    editMode.value = false;
  } catch (error) {
    console.error('Ошибка', error);
    alert('Ошибка обновления профиля');
  }
};

const updatePassword = async () => {
  try {
    await axios.post(
      'api/auth/users/set_password/',
      {
        new_password: profilePassword.value.new_password,
        current_password: profilePassword.value.current_password,
      },
      {
        headers: { Authorization: `Token ${token.token}` },
      }
    );
    alert('Пароль успешно изменён');
    profilePassword.value.new_password = '';
    profilePassword.value.current_password = '';
  } catch (error) {
    console.error('Ошибка', error);
    alert('Возникла ошибка');
  }
};

onMounted(profile);
</script>
