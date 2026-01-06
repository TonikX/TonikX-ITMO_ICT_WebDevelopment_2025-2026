<template>
  <div class="app-container">
    <header class="app-header">
      <select v-model="selectedClass" class="class-select">
        <option v-for="klass in Object.values(classes)" :key="klass.id" :value="klass.id">
          {{ klass.parallel }}-{{ klass.class_number }}
        </option>
      </select>
    </header>

    <button @click="openCreateModal" class="add-lesson-btn">Add Lesson</button>

    <main class="main-content">
      <div v-if="filteredLessons.length > 0" class="lesson-calendar">
        <div class="weekday-header" v-for="weekday in weekdays" :key="weekday">
          {{ weekday }}
        </div>
        <div
            v-for="lessonSlot in lessonSlots"
            :key="lessonSlot.id"
            class="lesson-slot"
        >
          <div v-if="lessonSlot.lesson" class="lesson-card">
            <a @click="openDetailsModal(lessonSlot.lesson)">
              <h3>{{ lessonSlot.lesson.subject.name }}</h3>
              <p><strong>Teacher:</strong> {{ lessonSlot.lesson.teacher.first_name }} {{ lessonSlot.lesson.teacher.last_name }}</p>
            </a>
          </div>
        </div>
      </div>

      <div v-else>
        <p>No lessons found for the selected class.</p>
      </div>
    </main>

    <CreateLessonModal
        v-if="isCreateModalVisible"
        @close="closeModal"
        @save="fetchLessons"
    />

    <EditLessonModal
        v-if="isEditModalVisible"
        :lesson="selectedLesson"
        @close="closeModal"
        @save="fetchLessons"
    />

    <DetailsLessonModal
        v-if="isDetailsModalVisible"
        :lesson="selectedLesson"
        @close="closeModal"
        @delete="deleteLesson"
        @edit="openEditModal"
    />
  </div>
</template>

<script>
import API from "@/axios";
import CreateLessonModal from "../components/CreateLessonModal.vue";
import EditLessonModal from "../components/EditLessonModal.vue";
import DetailsLessonModal from "../components/LessonDetailsModal.vue";

export default {
  components: {
    CreateLessonModal,
    EditLessonModal,
    DetailsLessonModal,
  },
  data() {
    return {
      lessons: [],
      classes: {},
      selectedClass: null,
      weekdays: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      lessonSlots: [],
      isCreateModalVisible: false,
      isEditModalVisible: false,
      isDetailsModalVisible: false,
      selectedLesson: null,
    };
  },
  computed: {
    filteredLessons() {
      return this.lessons.filter(
          (lesson) => lesson.klass === this.selectedClass
      );
    },
  },
  methods: {
    generateLessonSlots() {
      this.lessonSlots = [];
      for (let number = 1; number <= 7; number++) {
        this.weekdays.forEach((weekday) => {
          const lesson = this.filteredLessons.find(
              (l) => l.weekday === weekday && l.lesson_number === number
          );
          this.lessonSlots.push({
            id: `${weekday}-${number}`,
            lesson,
          });
        });
      }
    },
    async fetchLessons() {
      try {
        const response = await API.get("/lessons/");
        const classesResponse = await API.get("/classes/");
        this.classes = classesResponse.data.reduce((map, klass) => {
          map[klass.id] = klass;
          return map;
        }, {});
        this.lessons = response.data;
        if (!this.selectedClass) {
          this.selectedClass = Object.keys(this.classes)[0];
        }
        this.generateLessonSlots();
      } catch (error) {
        console.error("Error fetching lessons:", error);
      }
    },
    async deleteLesson(lessonId) {
      try {
        await API.delete(`/lessons/${lessonId}/`);
        this.lessons = this.lessons.filter((lesson) => lesson.id !== lessonId);
        this.generateLessonSlots();
      } catch (error) {
        console.error("Error deleting lesson:", error);
      }
    },
    openCreateModal() {
      this.isCreateModalVisible = true;
    },
    openEditModal(lesson) {
      this.selectedLesson = { ...lesson };
      this.isDetailsModalVisible = false;
      this.isEditModalVisible = true;
    },
    openDetailsModal(lesson) {
      this.selectedLesson = { ...lesson };
      this.isDetailsModalVisible = true;
      this.isEditModalVisible = false;
    },
    closeModal() {
      this.isCreateModalVisible = false;
      this.isEditModalVisible = false;
      this.isDetailsModalVisible = false;
    },
  },
  watch: {
    selectedClass() {
      this.generateLessonSlots();
    },
  },
  mounted() {
    this.fetchLessons();
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";

.lesson-calendar {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-auto-rows: 100px;
  gap: 10px;
}

.weekday-header {
  font-weight: bold;
  font-size: 18px;
  text-align: center;
  background-color: #f0f0f0;
  padding: 5px 0;
  border: 1px solid #ddd;
  line-height: 1.1;
}

.lesson-slot {
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  border-radius: 8px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.lesson-card {
  width: 100%;
  height: 100%;
  border: 1px solid transparent;
  border-radius: 8px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s, box-shadow 0.2s;
}

.lesson-card:hover {
  background-color: #f0f8ff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.lesson-card h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
}

.lesson-card p {
  margin: 4px 0 0;
  font-size: 16px;
  text-align: center;
  color: #555;
}

.lesson-card a {
  color: inherit;
  text-decoration: none;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.lesson-card a:hover {
  text-decoration: none;
}
</style>
