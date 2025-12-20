<template>
    <div>
      <h1>Бронирование</h1>
      <form @submit.prevent="submitBooking">
        <input v-model="name" placeholder="Ваше имя" required />
        <input v-model="room" placeholder="Тип номера" required />
        <button type="submit">Забронировать</button>
      </form>
    </div>
  </template>
  <script>
  export default {
    data() {
      return {
        name: '',
        room: '',
      };
    },
    methods: {
      submitBooking() {
        alert(`Бронирование успешно! ${this.name}, ваш номер: ${this.room}.`);
      },
    },
  };
  </script>
  <style scoped>
  form {
    display: flex;
    flex-direction: column;
    max-width: 300px;
  }
  input {
    margin-bottom: 10px;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  button {
    padding: 8px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>
  