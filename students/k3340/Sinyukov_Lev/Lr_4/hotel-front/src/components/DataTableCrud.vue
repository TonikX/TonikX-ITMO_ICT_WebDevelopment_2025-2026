<template>
  <v-card>
    <v-card-title class="d-flex align-center justify-space-between">
      <span>{{ title }}</span>
      <div class="d-flex ga-2">
        <v-btn variant="tonal" @click="load">Reload</v-btn>
        <v-btn @click="openCreate">Create</v-btn>
      </div>
    </v-card-title>

    <v-card-text>
      <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

      <v-data-table
        :headers="headers"
        :items="items"
        :loading="loading"
        item-key="id"
      >
        <template #item.actions="{ item }">
          <v-btn size="small" variant="text" @click="openEdit(item)">Edit</v-btn>
          <v-btn size="small" variant="text" color="red" @click="askDelete(item)">Delete</v-btn>
        </template>
      </v-data-table>
    </v-card-text>

    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ editing ? "Edit" : "Create" }}</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="save">
            <v-text-field
              v-for="f in formFields"
              :key="f.key"
              v-model="form[f.key]"
              :label="f.label"
              :type="f.type || 'text'"
            />
            <v-btn type="submit" :loading="saving">{{ editing ? "Save" : "Create" }}</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="confirm" max-width="420">
      <v-card>
        <v-card-title>Удалить?</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить запись id={{ deleting?.id }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="confirm=false">Cancel</v-btn>
          <v-btn color="red" @click="doDelete" :loading="deletingLoading">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { http } from "@/api/http";

const props = defineProps({
  title: { type: String, required: true },
  endpoint: { type: String, required: true },
  columns: { type: Array, required: true },
  formFields: { type: Array, required: true },
});

const headers = computed(() => [
  ...props.columns.map((c) => ({ title: c.title, key: c.key })),
  { title: "Actions", key: "actions", sortable: false },
]);

const items = ref([]);
const loading = ref(false);
const saving = ref(false);
const error = ref("");

const dialog = ref(false);
const editing = ref(false);
const form = ref({});
const editingId = ref(null);

const confirm = ref(false);
const deleting = ref(null);
const deletingLoading = ref(false);

async function load() {
  loading.value = true;
  error.value = "";
  try {
    const res = await http.get(props.endpoint);
    items.value = res.data;
  } catch (e) {
    error.value = JSON.stringify(e.response?.data || e.message);
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  editing.value = false;
  editingId.value = null;
  form.value = {};
  dialog.value = true;
}

function openEdit(item) {
  editing.value = true;
  editingId.value = item.id;
  form.value = { ...item };
  dialog.value = true;
}

async function save() {
  saving.value = true;
  error.value = "";
  try {
    if (editing.value) {
      await http.put(`${props.endpoint}${editingId.value}/`, form.value);
    } else {
      await http.post(props.endpoint, form.value);
    }
    dialog.value = false;
    await load();
  } catch (e) {
    error.value = JSON.stringify(e.response?.data || e.message);
  } finally {
    saving.value = false;
  }
}

function askDelete(item) {
  deleting.value = item;
  confirm.value = true;
}

async function doDelete() {
  deletingLoading.value = true;
  error.value = "";
  try {
    await http.delete(`${props.endpoint}${deleting.value.id}/`);
    confirm.value = false;
    await load();
  } catch (e) {
    error.value = JSON.stringify(e.response?.data || e.message);
  } finally {
    deletingLoading.value = false;
  }
}

onMounted(load);
</script>