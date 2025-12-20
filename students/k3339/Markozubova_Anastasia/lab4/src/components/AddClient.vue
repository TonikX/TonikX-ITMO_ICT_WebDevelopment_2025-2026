<template>
    <v-dialog v-model="show" max-width="600px">
      <v-card>
        <v-card-title>Добавить клиента</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="client.first_name"
              label="Имя"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="client.last_name"
              label="Фамилия"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="client.middle_name"
              label="Отчество"
            ></v-text-field>
            <v-text-field
              v-model="client.city"
              label="Город"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="client.passport_number"
              label="Номер паспорта"
              :rules="[rules.required]"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="close">Отмена</v-btn>
          <v-btn color="primary" :disabled="!valid" @click="saveClient">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  import { ref, watch } from "vue";
  import axios from "axios";
  import { tokenStore } from "@/stores/token.js";
  const tokenStorage = tokenStore();
  
  // Props для управления модальным окном
  const props = defineProps({
    modelValue: {
      type: Boolean,
      required: true,
    },
  });
  
  // Emit-событие для обновления родителя
  const emit = defineEmits(["update:modelValue", "refresh"]);
  
  // Локальные переменные
  const show = ref(props.modelValue);
  const client = ref({
    first_name: "",
    last_name: "",
    middle_name: "",
    city: "",
    passport_number: "",
  });
  const valid = ref(false);
  const rules = {
    required: (value) => !!value || "Обязательное поле",
  };
  
  
  // Синхронизация props и локального состояния
  watch(
    () => props.modelValue,
    (newVal) => (show.value = newVal)
  );
  
  watch(show, (newVal) => emit("update:modelValue", newVal));
  
  // Закрытие модального окна
  function close() {
    resetForm();
    show.value = false;
  }
  
  // Сброс формы
  function resetForm() {
    client.value = {
      first_name: "",
      last_name: "",
      middle_name: "",
      city: "",
      passport_number: "",
    };
    valid.value = false;
  }
  
  // Сохранение клиента
  async function saveClient() {
    try {
      await axios.post("/api/clients/", client.value, {
        headers: {
          Authorization: `Token ${tokenStorage.token}`,
        },
      });
      emit("refresh"); // Обновление списка клиентов
      close();
    } catch (error) {
      console.error("Ошибка сохранения клиента:", error);
    }
  }
  </script>
  