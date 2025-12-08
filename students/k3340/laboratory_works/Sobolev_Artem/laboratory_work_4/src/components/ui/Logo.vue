<template>
  <a
      class="logo"
      href="/"
      :class='customStyle ? "white-logo" : "default-logo"'
  >
    <span>
      КурКод
    </span>
  </a>
</template>

<script setup>
defineProps({
  customStyle: {
    type: Boolean,
    default: false
  }
})
</script>
<style lang="scss" scoped>
.logo {
  font-family: var(--font-family-logo), sans-serif;
  font-weight: 400;
  font-size: 32px;
}
.default-logo {
  color: var(--color);
}
.white-logo {
  color: var(--color-white);
  font-size: 40px;
}
</style>