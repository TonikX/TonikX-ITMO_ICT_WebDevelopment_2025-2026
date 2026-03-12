<template>
  <v-container>
    <h2>Запросы для библиотекаря</h2>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Книги, закрепленные за читателем</h3>
      <v-row>
        <v-col cols="12" md="6">
          <v-select
            v-model="selectedReaderId"
            :items="readers"
            item-title="full_name"
            item-value="id"
            label="Выберите читателя"
          />
        </v-col>
        <v-col cols="12" md="6" class="d-flex align-end">
          <v-btn color="primary" @click="loadReaderBooks" :disabled="!selectedReaderId">
            Показать книги
          </v-btn>
        </v-col>
      </v-row>
      <v-list v-if="readerBooks.length">
        <v-list-item v-for="(b, idx) in readerBooks" :key="idx">
          <v-list-item-title>{{ b }}</v-list-item-title>
        </v-list-item>
      </v-list>
      <p v-else class="text-muted">Нет данных для выбранного читателя.</p>
    </section>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Читатели с просроченными книгами (&gt; 1 месяца)</h3>
      <v-btn color="primary" @click="loadOverdueReaders">Загрузить список</v-btn>
      <v-list v-if="overdueReaders.length" class="mt-3">
        <v-list-item v-for="(r, idx) in overdueReaders" :key="idx">
          <v-list-item-title>{{ r }}</v-list-item-title>
        </v-list-item>
      </v-list>
      <p v-else class="text-muted mt-3">Нет данных.</p>
    </section>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Читатели с редкими книгами (копий ≤ 2)</h3>
      <v-btn color="primary" @click="loadRareBooksReaders">Загрузить</v-btn>
      <v-simple-table class="mt-3" v-if="rareBooksReaders.length">
        <thead>
          <tr>
            <th>Читатель</th>
            <th>Книга</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, idx) in rareBooksReaders" :key="idx">
            <td>{{ row.reader }}</td>
            <td>{{ row.book }}</td>
          </tr>
        </tbody>
      </v-simple-table>
      <p v-else class="text-muted mt-3">Нет данных.</p>
    </section>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Количество читателей младше 20 лет</h3>
      <v-btn color="primary" @click="loadUnder20">Посчитать</v-btn>
      <p class="mt-3" v-if="under20Count !== null">
        Всего читателей младше 20 лет: <strong>{{ under20Count }}</strong>
      </p>
    </section>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Статистика по образованию (в %)</h3>
      <v-btn color="primary" @click="loadEducationStats">Показать</v-btn>
      <v-simple-table class="mt-3" v-if="educationStats">
        <thead>
          <tr>
            <th>Категория</th>
            <th>Процент</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Начальное</td>
            <td>{{ educationStats.primary }}%</td>
          </tr>
          <tr>
            <td>Среднее</td>
            <td>{{ educationStats.secondary }}%</td>
          </tr>
          <tr>
            <td>Высшее</td>
            <td>{{ educationStats.higher }}%</td>
          </tr>
          <tr>
            <td>Ученая степень</td>
            <td>{{ educationStats.degree }}%</td>
          </tr>
        </tbody>
      </v-simple-table>
      <p v-else class="text-muted mt-3">Нет данных.</p>
    </section>
  </v-container>
</template>

<script>
import api from "../api/index.js";

export default {
  data() {
    return {
      readers: [],
      selectedReaderId: null,
      readerBooks: [],
      overdueReaders: [],
      rareBooksReaders: [],
      under20Count: null,
      educationStats: null,
    };
  },
  async mounted() {
    try {
      const res = await api.getReaders();
      this.readers = res.data;
    } catch (e) {
      console.error(e);
    }
  },
  methods: {
    async loadReaderBooks() {
      if (!this.selectedReaderId) return;
      try {
        const res = await api.getReaderBooks(this.selectedReaderId);
        this.readerBooks = res.data;
      } catch (e) {
        console.error(e);
        this.readerBooks = [];
      }
    },
    async loadOverdueReaders() {
      try {
        const res = await api.getIssuesOverdue();
        this.overdueReaders = res.data;
      } catch (e) {
        console.error(e);
        this.overdueReaders = [];
      }
    },
    async loadRareBooksReaders() {
      try {
        const res = await api.getRareBooksReaders();
        this.rareBooksReaders = res.data;
      } catch (e) {
        console.error(e);
        this.rareBooksReaders = [];
      }
    },
    async loadUnder20() {
      try {
        const res = await api.getReadersUnder20();
        this.under20Count = res.data.readers_under_20 ?? null;
      } catch (e) {
        console.error(e);
        this.under20Count = null;
      }
    },
    async loadEducationStats() {
      try {
        const res = await api.getEducationStats();
        this.educationStats = {
          primary: res.data["primary_%"],
          secondary: res.data["secondary_%"],
          higher: res.data["higher_%"],
          degree: res.data["degree_%"],
        };
      } catch (e) {
        console.error(e);
        this.educationStats = null;
      }
    },
  },
};
</script>

