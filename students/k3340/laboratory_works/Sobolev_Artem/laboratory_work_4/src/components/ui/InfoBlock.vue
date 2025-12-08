<template>
  <a
      class="info-block"
      :href="href"
  >
    <span class="info-block__title">
      {{ title }}
    </span>
    <div class="info-block__container">
       <span v-if="subTitle" class="info-block__subtitle">
      {{ subTitle }}
    </span>
      <span v-if="count && !loading" class="info-block__count">
      {{ count }}
    </span>
      <Loader v-if="loading" :width="28" :height="28" color="var(--color-white)" />
    </div>
  </a>
</template>

<script setup>
import Loader from "@/components/ui/Loader.vue";

defineProps({
  title: {
    type: String,
    required: true
  },
  href: {
    type: String,
    required: true
  },
  subTitle: {
    type: String,
    required: false
  },
  count: {
    type: String,
    required: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})
</script>

<style lang="scss" scoped>
.info-block {
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  width: 100%;
  box-sizing: border-box;
  gap: 18px;
  color: var(--color-white);

  &__container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  &__title {
    font-weight: 600;
    font-size: 14px;
  }

  &__subtitle {
    font-weight: 500;
    opacity: 0.8;
    font-size: 14px;
  }

  &__count {
    font-weight: 600;
    font-size: 23px;
  }
}
</style>