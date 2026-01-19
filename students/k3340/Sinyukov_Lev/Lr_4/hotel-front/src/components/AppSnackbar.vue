<template>
  <v-snackbar
    v-model="ui.snackbar.show"
    :timeout="ui.snackbar.timeout"
    :color="ui.snackbar.color"
  >
    {{ ui.snackbar.text }}
    <template #actions>
      <v-btn variant="text" @click="ui.close()">OK</v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { useUiStore } from "@/stores/ui";
const ui = useUiStore();
</script>