<template>
  <v-row justify="center" class="mt-8">
    <v-col cols="12" md="6">
      <v-card title="Profile">
        <v-card-text>
          <v-text-field v-model="user.username" label="Username" readonly />
          <v-text-field v-model="user.email" label="Email" />
          <v-text-field v-model="user.first_name" label="First Name" />
          <v-text-field v-model="user.last_name" label="Last Name" />
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
const user = ref({})
onMounted(async () => { const { data } = await api.get('/auth/users/me/'); user.value = data })
const save = async () => {
  await api.patch('/auth/users/me/', {
    email: user.value.email,
    first_name: user.value.first_name,
    last_name: user.value.last_name,
  })
}
</script>
