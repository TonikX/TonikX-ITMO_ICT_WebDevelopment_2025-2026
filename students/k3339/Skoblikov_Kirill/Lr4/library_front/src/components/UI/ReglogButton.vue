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
  color: #7a66ea;
  width: 430px;
  height: 50px;
  font-size: 28px;
  font-weight: bold;
  border-radius: 20px;
  border: 2px solid #7a66ea;
  background: white;
  margin: 10px;
}

.btn:hover {
  background: rgba(233, 224, 250, 0.94);
  border-color: rgba(117, 85, 177, 0.91);
  transform: translateY(-2px);
}
</style>