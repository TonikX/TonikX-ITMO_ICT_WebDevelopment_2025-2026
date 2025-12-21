<!-- components/CarDetailsDialog.vue -->
<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <v-icon icon="mdi-car-info" size="24" class="mr-2"></v-icon>
      <span class="text-h5">Детали автомобиля</span>
      <v-spacer></v-spacer>
      <v-btn icon @click="$emit('close')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="12" md="6">
          <v-img
            :src="carImage"
            height="250"
            cover
            class="rounded-lg"
          ></v-img>
        </v-col>

        <v-col cols="12" md="6">
          <v-list lines="two" density="compact">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-car" class="mr-3"></v-icon>
              </template>
              <v-list-item-title>Марка и модель</v-list-item-title>
              <v-list-item-subtitle class="text-h6">
                {{ car.car?.car_info?.brand }} {{ car.car?.car_info?.model }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-numeric" class="mr-3"></v-icon>
              </template>
              <v-list-item-title>Госномер</v-list-item-title>
              <v-list-item-subtitle class="text-body-1 font-weight-bold">
                {{ car.license_plate }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-barcode" class="mr-3"></v-icon>
              </template>
              <v-list-item-title>VIN-код</v-list-item-title>
              <v-list-item-subtitle>
                {{ car.vincode }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-calendar" class="mr-3"></v-icon>
              </template>
              <v-list-item-title>Год выпуска</v-list-item-title>
              <v-list-item-subtitle>
                {{ car.year }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-palette" class="mr-3"></v-icon>
              </template>
              <v-list-item-title>Цвет</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip size="small" :color="getColorCode(car.color)">
                  {{ car.color }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-currency-rub" class="mr-3"></v-icon>
              </template>
              <v-list-item-title>Цена проката</v-list-item-title>
              <v-list-item-subtitle class="text-h5 text-primary">
                {{ formatPrice(car.price) }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>

      <!-- Технические характеристики -->
      <v-expansion-panels class="mt-4">
        <v-expansion-panel>
          <v-expansion-panel-title>
            <v-icon icon="mdi-cogs" class="mr-2"></v-icon>
            Технические характеристики
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-row v-if="car.car">
              <v-col cols="12" md="6">
                <v-list density="compact">
                  <v-list-item>
                    <v-list-item-title>Тип КПП</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ getTransmissionText(car.car.transmission) }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Тип топлива</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ getFuelTypeText(car.car.fuel_type) }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Объем двигателя</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ car.car.engine_volume }} л
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>
              <v-col cols="12" md="6">
                <v-list density="compact">
                  <v-list-item>
                    <v-list-item-title>Мощность</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ car.car.horsepower }} л.с.
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Количество мест</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ car.car.capacity }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Расход топлива</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ car.car.fuel_consumption }} л/100км
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        color="primary"
        @click="$emit('close')"
      >
        Закрыть
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  car: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])

const carImage = computed(() => {
  const brand = props.car.car?.car_info?.brand?.toLowerCase() || 'car'
  return `https://source.unsplash.com/featured/600x400/?${brand},car,auto`
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const getColorCode = (color) => {
  const colorMap = {
    'черный': 'black',
    'белый': 'white',
    'серебристый': 'grey-lighten-2',
    'серый': 'grey',
    'синий': 'blue',
    'красный': 'red',
    'зеленый': 'green'
  }
  return colorMap[color?.toLowerCase()] || 'grey'
}

const getTransmissionText = (transmission) => {
  const types = {
    'A': 'Автоматическая',
    'M': 'Механическая'
  }
  return types[transmission] || transmission
}

const getFuelTypeText = (fuelType) => {
  const types = {
    1: 'АИ-92',
    2: 'АИ-95',
    3: 'АИ-98',
    4: 'АИ-100',
    5: 'ДТ',
    6: 'Электрический',
    7: 'Гибрид'
  }
  return types[fuelType] || 'Неизвестно'
}
</script>