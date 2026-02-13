<template>
  <button class="btn">
    <slot></slot>
  </button>
</template>

<script>
export default {

}
</script>

<style scoped>
.btn {
  color: #6f29e0dc;
  width: 700px;
  height: 80px;
  font-size: 28px;
  font-weight: bold;
  border-radius: 64px;
  border: 2px solid #6f29e0dc;
  background: white;
  margin: 10px;
}

.btn:hover {
  background: rgba(233, 224, 250, 0.94);
  border-color: rgba(117, 85, 177, 0.91);
  transform: translateY(-2px);
}
</style>