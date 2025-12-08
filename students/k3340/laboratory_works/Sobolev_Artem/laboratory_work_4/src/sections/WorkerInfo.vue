<template>
  <div class="worker page-block">
    <div class="worker__img-container">
      <img class="worker__img" :src="photo" alt="Worker photo"/>
    </div>

    <div class="worker__container">
      <div class="worker__info">
        <h2>Основная информация</h2>

        <h3 class="h2">ФИО</h3>
        <span>{{ firstName }} {{ name }} {{ patronymic }}</span>

        <h3 class="h2">Должность</h3>
        <span>{{ position }}</span>

        <div class="salary-row">
          <h3 class="h2">Заработная плата</h3>
          <Button
              :icon-name="isHiddenSalary ? 'show' : 'hide'"
              :icon-width="19"
              :icon-height="19"
              @click="toggleSalary"
          />
        </div>
        <span>{{ isHiddenSalary ? maskedSalary : salary + ' ₽' }}</span>
      </div>

      <div class="worker__info" style="min-width: 20%;">
        <h2>Контакты</h2>

        <div class="row">
          <h3 class="h2">Почта</h3>
          <Button
              :icon-name="isHiddenEmail ? 'show' : 'hide'"
              :icon-width="19"
              :icon-height="19"
              @click="toggleEmail"
          />
        </div>
        <span class="break">{{ isHiddenEmail ? maskedEmail : email }}</span>

        <div class="row">
          <h3 class="h2">Телефон</h3>
          <Button
              :icon-name="isHiddenPhone ? 'show' : 'hide'"
              :icon-width="20"
              :icon-height="20"
              @click="togglePhone"
          />
        </div>
        <span>{{ isHiddenPhone ? maskedPhone : phone }}</span>
      </div>

      <div class="worker__info">
        <h2>Документы</h2>
        <h3 class="h2">Паспорт</h3>
        <span class="text-ellipsis"></span>

        <h3 class="h2">Договор</h3>
        <span class="text-ellipsis"></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed} from "vue";
import Button from "@/components/ui/Button.vue";

const props = defineProps({
  photo: String,
  firstName: String,
  name: String,
  patronymic: String,
  position: String,
  salary: [Number, String],
  phone: String,
  email: String,
  status: String
});

const isHiddenPhone = ref(true);
const isHiddenEmail = ref(true);
const isHiddenSalary = ref(true);

const maskedPhone = computed(() =>
    props.phone?.replace(/\d/g, "*") || "-"
);
const maskedEmail = computed(() =>
    props.email?.replace(/[^@]/g, "*") || "-"
);
const maskedSalary = computed(() =>
    props.salary?.toString().replace(/\d/g, "*")
);

const togglePhone = () => (isHiddenPhone.value = !isHiddenPhone.value);
const toggleEmail = () => (isHiddenEmail.value = !isHiddenEmail.value);
const toggleSalary = () => (isHiddenSalary.value = !isHiddenSalary.value);
</script>

<style scoped lang="scss">
.worker {
  display: flex;
  flex-direction: row;
  align-items: flex-start;

  &__container {
    width: 70%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-inline: auto;
    gap: 64px;
  }

  &__info {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  &__img-container {
    width: 14vw;
    height: 14vw;
    overflow: hidden;
    border-radius: 8px;
  }

  &__img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
}

.row,
.salary-row {
  display: flex;
  flex-direction: row;
  gap: 16px;
  align-items: center;
}

.break {
  max-width: 250px;
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: anywhere;
}
</style>
