<template>
  <div class="info-graph">
    <div class="info-graph__header">
      <h2 class="info-graph__title">
        {{ title }}
      </h2>
      <Button
          :href="href"
          class="info-graph__button"
          icon-name="arrow-right"
          :icon-width="28"
          :icon-height="28"
      />
    </div>
    <div class="info-graph__image-container">
      <img
          :src="image"
          alt=""
      />
    </div>
  </div>
</template>

<script setup>
import Button from "@/components/ui/Button.vue";

defineProps({
  title: {
    type: String,
    required: true,
  },
  href: {
    type: String,
    required: true,
  },
  image: {
    type: String,
    required: true,
  }
})
</script>

<style lang="scss" scoped>
.info-graph {
  color: var(--color);
  &__header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20px;
  }

  &__title {
    font-size: 16px;
  }

  &__button {
    color: var(--color);
  }
}
</style>