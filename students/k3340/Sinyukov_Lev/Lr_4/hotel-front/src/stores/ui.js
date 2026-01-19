import { defineStore } from "pinia";

export const useUiStore = defineStore("ui", {
  state: () => ({
    snackbar: {
      show: false,
      text: "",
      color: "success", // success | error | info
      timeout: 2500,
    },
  }),
  actions: {
    toast(text, color = "success", timeout = 2500) {
      this.snackbar = { show: true, text, color, timeout };
    },
    close() {
      this.snackbar.show = false;
    },
  },
});