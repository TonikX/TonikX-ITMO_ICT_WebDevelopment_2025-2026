<template>
  <div class="account">
    <div class="account__first-row">
      <div class="account__block">
        <div class="account__header">
          <h2 class="account__title">Основная информация</h2>
          <Button
              label="Редактировать"
              mode="violet"
              location="block-action"
          />
        </div>

        <div class="account__content page-block">
          <div class="account__img-container">

          </div>

          <div class="account__info">
            <span class="h2 text-ellipsis">Фамилия</span>
            <span class="h2 text-ellipsis">Имя</span>
            <span class="h2 text-ellipsis">Отчество</span>
          </div>

          <div class="account__info">
            <span class="h2">Директор предприятия</span>
            <span style="display: flex; flex-direction: row; gap: 16px; align-items: center;">
              <span class="account__info-text text-ellipsis" :class="{ 'letter-spacing-email': isHiddenEmail }"
                    style="width: 20vw">
                {{ isHiddenEmail ? maskedEmail : email }}
              </span>
              <Button
                  style="align-self: flex-end; margin-left: auto"
                  :icon-name="isHiddenEmail ? 'show' : 'hide'"
                  :icon-width="20"
                  :icon-height="20"
                  @click="toggleEmail"
              />
            </span>
            <span style="display: flex; flex-direction: row; gap: 16px; align-items: center;">
              <span class="account__info-text" :class="{ 'letter-spacing-phone': isHiddenPhone }">
                {{ isHiddenPhone ? maskedPhone : phone }}
              </span>
              <Button
                  style="align-self: flex-end; margin-left: auto"
                  :icon-name="isHiddenPhone ? 'show' : 'hide'"
                  :icon-width="20"
                  :icon-height="20"
                  @click="togglePhone"
              />
            </span>
          </div>
        </div>
      </div>

      <div class="account__block">
        <div class="account__header">
          <h2 class="account__title">Безопасность</h2>
          <Button
              label="Настроить"
              mode="violet"
              location="block-action"
          />
        </div>
        <div class="account__content page-block">

        </div>
      </div>
    </div>
    <div class="account__first-row">

      <div class="account__block">
        <div class="account__header">
          <h2 class="account__title">Уведомления</h2>
        </div>
        <div class="account__content page-block">

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Button from "@/components/ui/Button.vue";
import {computed, ref} from "vue";

const phone = ref("+7 (999) 123-45-67")
const email = ref("emailemailemail@gmail.com")

const isHiddenPhone = ref(true)
const isHiddenEmail = ref(true)

const maskedPhone = computed(() => {
  return phone.value.replace(/\d/g, '*')
})

const maskedEmail = computed(() => {
  return email.value.replace(/[^@.]/g, '*')
})

function togglePhone() {
  isHiddenPhone.value = !isHiddenPhone.value
}

function toggleEmail() {
  isHiddenEmail.value = !isHiddenEmail.value
}
</script>

<style lang="scss" scoped>
.account {
  &__first-row {
    display: grid;
    grid-template-columns: 1.8fr 1fr;
    gap: 32px;
    margin-bottom: 32px;
  }

  &__header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  &__content {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    gap: 16px;
  }

  &__info {
    display: flex;
    flex-direction: column;
    gap: 24px;

    &-text {
      text-wrap: wrap;
    }
  }

  &__img-container {
    width: 10vw;
    height: 10vw;
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

.letter-spacing-email {
  letter-spacing: 0.155em;
}

.letter-spacing-phone {
  letter-spacing: 0.1em;
}
</style>