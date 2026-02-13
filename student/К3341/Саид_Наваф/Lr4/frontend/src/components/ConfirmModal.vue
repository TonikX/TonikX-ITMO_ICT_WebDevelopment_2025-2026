<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal">
      <h3>{{ title || 'Confirm' }}</h3>
      <p class="small">{{ message || 'Are you sure?' }}</p>
      <div style="display:flex; gap:8px; justify-content:flex-end; margin-top:12px;">
        <button class="btn secondary" @click="close">Cancel</button>
        <button class="btn" @click="confirm">Confirm</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfirmModal",
  props: { title: String, message: String },
  emits: ["confirm","close"],
  methods: {
    confirm(){ this.$emit('confirm'); this.$emit('close'); },
    close(){ this.$emit('close'); }
  }
}
</script>