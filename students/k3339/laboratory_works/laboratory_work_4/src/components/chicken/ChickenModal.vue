  <script setup>
  import {ref, watch} from "vue";


const props = defineProps({
  modelValue: { type: Boolean, required: true },
  chickenData: { type: Object },
  breeds: { type: Array, default: () => [] },
  cells: { type: Array, default: () => [] },
  mode: { type: String, default: "add" },
});


  const emits = defineEmits(["update:modelValue", "submit-chicken"]);

  const formData = ref({...(props.chickenData ?? {}) });

  watch(
      () => props.chickenData,
      (newVal) => {
        formData.value = {...(newVal ?? {}) };
      }
  );


  function closeModal() {
    emits("update:modelValue", false);
  }


  function handleSubmit() {
    const toId = (v) => (v && typeof v === "object" ? v.id : v)

    const cellId = toId(formData.value.cell)
    const breedId = toId(formData.value.breed)
    const dietId = toId(formData.value.diet)

    if (props.mode === "add" && !cellId) {
      alert("Выберите клетку")
      return
    }
    if (!breedId) {
      alert("Выберите породу")
      return
    }

    emits("submit-chicken", {
      ...formData.value,
      weight: Number(formData.value.weight),
      age: Number(formData.value.age),
      egg_performance_month: Number(formData.value.egg_performance_month),
      cell: cellId,
      breed: breedId,
      diet: dietId,
    })

    closeModal()
  }

  </script>

  <template>
    <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
      <v-card>
        <v-card-title>{{ mode === "add" ? "Добавить курицу" : "Редактировать курицу" }}</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="handleSubmit">
            <v-text-field v-model="formData.weight" label="Вес" required type="number"></v-text-field>
            <v-text-field v-model="formData.age" label="Возраст" required type="number"></v-text-field>

            <v-select
              v-model="formData.breed"
              :items="breeds"
              item-title="name"
              item-value="id"
              label="Порода"
              required
            />

            <v-select
              v-model="formData.cell"
              :items="cells"
              item-title="cell_code"
              item-value="id"
              label="Клетка"
              required
            />
            
            <v-text-field
              v-model="formData.egg_performance_month"
              label="Яйценоскость за месяц"
              required
              type="number"
            ></v-text-field>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
          <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>