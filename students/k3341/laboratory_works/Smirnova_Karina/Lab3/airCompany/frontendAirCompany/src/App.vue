<template>
  <div id="app">
    <Header />
    <router-view />
  </div>
</template>

<script>
import Header from './components/Header.vue';
export default {
  name: 'App',
  components: {
    Header,
  }
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  padding-bottom: 20px;
  min-height: 100vh;
}
</style>