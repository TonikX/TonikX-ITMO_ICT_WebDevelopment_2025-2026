<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal">
      <h2 class="modal-title">Подтверждение выхода</h2>

      <Button
          class="modal-close"
          @click="close"
          icon-name="close"
          icon-width="32"
          icon-height="32"
      />

      <div class="modal-content">
        <p class="modal-text">Вы действительно хотите выйти из системы?</p>

        <div class="modal-actions">
          <Button
              label="Остаться"
              mode="violet-no-switch"
              location="block-action"
              @click="stay"
          />

          <Button
              label="Выйти"
              mode="violet"
              location="block-action"
              @click="confirmLogout"
              :loading="loading"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Button from "@/components/ui/Button.vue";
import { logoutUser } from "@/api/auth.js";

const emit = defineEmits(["close", "confirm"]);

const router = useRouter();
const loading = ref(false);

const close = () => {
  emit("close");
};

const stay = () => {
  close();
};

const confirmLogout = async () => {
  loading.value = true;
  try {
    logoutUser();

    close();

    await router.push('/sign');


    emit("confirm");
  } catch (error) {
    console.error("Ошибка при выходе:", error);
    await router.push('/sign');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: var(--section-bg);
  padding: 36px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  flex-direction: column;
}

.modal-title {
  font-size: 24px;
  padding-bottom: 24px;
  color: var(--color);
  margin: 0;
  text-align: center;
}

.modal-close {
  position: absolute;
  top: 12px;
  right: 12px;
  background: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.modal-content {
  width: 100%;
  text-align: center;
}

.modal-text {
  font-size: 16px;
  color: var(--color);
  margin-bottom: 32px;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;

  @media (max-width: 480px) {
    flex-direction: column;
    align-items: center;
  }
}

.modal-actions .button {
  min-width: 150px;
}

.violet-no-switch {
  background-color: var(--color-section-contrast-light);
  color: var(--color-white);
}

.violet {
  background-color: var(--contrast);
  color: var(--color-white);
}

.block-action {
  font-weight: 600;
  font-size: 14px;
  width: 194px;
  border-radius: 8px;
  padding-block: 8px;
}
</style>