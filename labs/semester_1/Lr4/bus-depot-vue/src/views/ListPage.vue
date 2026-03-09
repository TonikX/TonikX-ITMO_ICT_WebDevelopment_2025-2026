<script>
import Header from '@/components/Header.vue';
import { titles, namingFunctions } from '@/assets/types';

export default {
    name: 'ListPage',
    props: {
        type: {
            type: String,
            required: true
        }
    },
    components: {
        Header
    },
    computed: {
        pageTitle() {
            return titles[this.type] || this.type;
        },
        apiUrl() {
            const baseUrl = 'http://127.0.0.1:8000/bus-depot';
            return `${baseUrl}/${this.type}/`;
        },
        deleteUrl() {
            const baseUrl = 'http://127.0.0.1:8000/bus-depot';
            return (id) => `${baseUrl}/${this.type}/${id}/`;
        },
    },
    data() {
        return {
            items: [],
            loading: false,
            error: null
        }
    },
    methods: {
        async fetchItems() {
            this.loading = true;
            this.error = null;

            const token = localStorage.getItem('auth_token');

            if (!token) {
                this.error = 'Ошибка авторизации. Токен не найден.';
                this.loading = false;
                return;
            }

            try {
                const response = await fetch(this.apiUrl, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`Ошибка HTTP: ${response.status}`);
                }

                this.items = await response.json();

                for (const item of this.items) {
                    if (namingFunctions[this.type]) {
                        item.displayName = await namingFunctions[this.type](item);
                    } else {
                        item.displayName = `ID: ${item.id}`;
                    }
                }
            } catch (err) {
                this.error = `Не удалось загрузить данные: ${err.message}`;
                console.error('Ошибка загрузки:', err);
            } finally {
                this.loading = false;
            }
        },
        async deleteItem(id, name) {
            if (!confirm(`Вы уверены, что хотите удалить '${name}'`)) {
                return;
            }
            const token = localStorage.getItem('auth_token');
            const response = await fetch(this.deleteUrl(id), {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            if (response.ok) {
                this.items = this.items.filter(item => item.id !== id);

            } else {
                alert("При удалении элемента возникла ошибка");
            }
        },
        goToAddPage() {
            this.$router.push(`/list/${this.type}/add`)
        }
    },
    mounted() {
        this.fetchItems();
    },
}
</script>


<template>
<v-app>
  <Header />
  
  <v-main>
    <v-container>
      <v-row>
        <v-col>
          <v-btn
            text
            plain
            :to="{ path: '/main' }"
            class="mb-4"
          >
            <v-icon>mdi-arrow-left</v-icon>
            Назад
          </v-btn>
          
          <v-card flat>
            <v-card-title class="text-h4">
              {{ pageTitle }}
            </v-card-title>
            
            <v-card-text>
              <div v-if="loading" class="text-center py-8">
                <v-progress-circular indeterminate />
              </div>
              
              <div v-else-if="error" class="text-center py-8">
                <v-alert type="error" text>
                  {{ error }}
                </v-alert>
              </div>
              
              <div v-else-if="items.length === 0" class="text-center py-8">
                <v-alert type="info" text>
                  Элементы не найдены
                </v-alert>
              </div>
              
              <div v-else>
                <v-btn
                  color="primary"
                  class="mb-4"
                  @click="goToAddPage"
                >
                  + Добавить
                </v-btn>
                
                <v-list>
                  <v-list-item
                    v-for="item in items"
                    :key="item.id"
                  >

                    <v-list-item-title>
                      {{ item.displayName }}
                    </v-list-item-title>

                    <v-list-item-action>
                      <v-btn
                        :to="{ name: 'ItemPage', params: { type: type, id: item.id } }"
                        class="mr-2"
                        color="grey lighten"
                      >
                        Подобнее
                      </v-btn>
                      
                      <v-btn
                        :to="{ name: 'EditPage', params: { type: type, id: item.id } }"
                        class="mr-2"
                        color="grey lighten"
                      >
                        Изменить
                      </v-btn>
                      
                      <v-btn
                        color="error"
                        @click="deleteItem(item.id, item.displayName)"
                      >
                        Удалить
                      </v-btn>
                    </v-list-item-action>
                  </v-list-item>
                </v-list>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</v-app>
</template>
