<script setup>
import {useRoute} from 'vue-router'
import Header from './components/layouts/Header.vue'
import Sidebar from "@/components/layouts/Sidebar.vue";
import Content from "@/components/layouts/Content.vue";
import {uiStore} from "@/stores/ui.js";

const route = useRoute()
const ui = uiStore()
const hiddenLayoutRoutes = ['/sign', '/register']
</script>

<template>
  <Header
      v-if="!hiddenLayoutRoutes.includes(route.path)"
      @toggle="ui.toggleSidebar()"
  />
  <div
      class="wrapper"
      :class="{ 'no-layout': hiddenLayoutRoutes.includes(route.path) }"
  >
    <Sidebar
        :isClosed="ui.isSidebarClosed"
        v-if="!hiddenLayoutRoutes.includes(route.path)"
    />
    <Content>
      <RouterView/>
    </Content>
  </div>
</template>

<style lang="scss" scoped>
.wrapper {
  display: flex;
  width: 100%;
  overflow-x: hidden;
  margin-top: 79px;
  height: calc(100vh - 79px);

  &.no-layout {
    margin-top: 0;
    height: 100vh;
  }
}
</style>
