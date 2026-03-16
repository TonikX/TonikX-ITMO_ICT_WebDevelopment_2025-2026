<script>
    import Header from '@/components/Header.vue';

    export default {
        components: {
            Header
        },
        data() {
            return {
                menuItems: [
                    { type: 'bus-types', title: 'Типы автобусов' },
                    { type: 'buses', title: 'Автобусы' },
                    { type: 'routes', title: 'Маршруты' },
                    { type: 'drivers', title: 'Водители' },
                    { type: 'driver-assignments', title: 'Назначения водителей' },
                    { type: 'bus-statuses', title: 'Статусы автобусов' }
                ],
            }
        },
    }
</script>


<template>
  <v-container class="pa-4">
    <Header />
    
    <v-row justify="center" class="mb-8">
      <v-col cols="12" class="text-center">
        <h1 class="text-h4 font-weight-medium">Автобусный парк</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="8" offset-md="2" lg="6" offset-lg="3">
        <v-list>
          <v-list-item
            v-for="item in menuItems"
            :key="item.type"
            :to="{ name: 'ListPage', params: { type: item.type } }"
            class="mb-2"
          >
            <v-list-item-title class="text-body-1">
              {{ item.title }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>
