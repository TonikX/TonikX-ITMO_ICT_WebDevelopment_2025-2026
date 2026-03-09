<script>
import Header from '@/components/Header.vue';
import { fields, foreignKeys2, namingFunctions, choices } from '@/assets/types.js';

export default {
    name: "AddPage",
    props: {
        type: {
            type: String,
            required: true
        }
    },
    components: {
        Header
    },
    data() {
        return {
            formData: {},
            foreignKeyOptions: {},
        }
    },
    computed: {
        fieldsForType() {
            return fields[this.type] || [];
        },
        apiBaseUrl() {
            return 'http://127.0.0.1:8000/bus-depot';
        },
        foreignKeysForType() {
            return foreignKeys2[this.type] || {};
        },
    },
    methods: {
        isForeignKey(field) {
            return field in this.foreignKeysForType;
        },
        isChoiceField(field) {
            return field in choices;
        },
        getOptionsForField(field) {
            return this.foreignKeyOptions[field] || [];
        },
        getChoicesForField(field) {
            return choices[field] || [];
        },
        async loadForeignKeyOptions() {
            const promises = Object.entries(this.foreignKeysForType).map(async ([field, targetType]) => {
                const token = localStorage.getItem('auth_token');
                const response = await fetch(`${this.apiBaseUrl}/${targetType.replaceAll('_', '-')}/`, {
                    headers: {
                        'Authorization': `Token ${token}`
                    }
                });
                const items = await response.json();
                const optionPromises = items.map(async (item) => {
                    const namingFunc = namingFunctions[targetType.replaceAll('_', '-')];
                    let name = '';
                    name = await namingFunc(item);
                    return {
                        id: item.id,
                        name: name
                    };
                });
                const options = await Promise.all(optionPromises);
                this.foreignKeyOptions[field] = options;
            });
            await Promise.all(promises);
        },
        async handleSubmit() {
            const token = localStorage.getItem('auth_token');
            const requestData = { ...this.formData };
            Object.keys(this.foreignKeysForType).forEach(field => {
                const options = this.getOptionsForField(field);
                const selectedOption = options.find(opt => opt.name === requestData[field]);
                if (selectedOption) {
                    requestData[field] = selectedOption.id;
                }
            });
            const response = await fetch(`${this.apiBaseUrl}/${this.type}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify(requestData)
            });
            if (!response.ok) {
                throw new Error(`Ошибка сервера: ${response.status}`);
            }
            this.$router.push(`/list/${this.type}`);
        },
    },
    watch: {
        type: {
            immediate: true,
            handler() {
                this.foreignKeyOptions = {};
                this.formData = {};
                this.loadForeignKeyOptions();
            }
        }
    }
}
</script>


<template>
  <Header />
  
  <v-container style="max-width: 800px;">
    <v-btn
      class="mb-4"
      @click="$router.go(-1)"
    >
      <v-icon>mdi-arrow-left</v-icon>
      Отмена
    </v-btn>

    <v-card flat>
      <v-card-title class="text-h5">
        Добавление {{ type }}
      </v-card-title>

      <v-form @submit.prevent="handleSubmit">
        <v-card-text>
          <v-row>
            <v-col
              v-for="field in fieldsForType"
              :key="field"
              cols="12"
            >
              <v-select
                v-if="isForeignKey(field)"
                v-model="formData[field]"
                :label="field"
                :items="getOptionsForField(field).map(opt => opt.name)"
                clearable
              />

              <v-select
                v-else-if="isChoiceField(field)"
                v-model="formData[field]"
                :label="field"
                :items="getChoicesForField(field)"
                clearable
              />

              <v-text-field
                v-else
                v-model="formData[field]"
                :label="field"
                clearable
              />
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-btn
            type="submit"
            color="primary"
          >
            Создать
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>
