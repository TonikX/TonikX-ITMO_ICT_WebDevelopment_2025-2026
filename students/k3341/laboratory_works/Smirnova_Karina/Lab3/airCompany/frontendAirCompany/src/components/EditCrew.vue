<template>
  <div class="edit-crew">
    <div class="content-wrapper">
      <h1>Редактирование команды №{{ crew.id }}</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-section">
            <h3>Участники команды</h3>
            <p class="section-description">Выберите участников, которые входят в состав команды</p>

            <div class="members-list">
              <div class="member-checkbox" v-for="member in allMembers" :key="member.id">
                <label :for="`member-${member.id}`" class="checkbox-label">
                  <input
                    type="checkbox"
                    :id="`member-${member.id}`"
                    :value="member.id"
                    v-model="selectedMemberIds"
                  />
                  <span class="member-info">
                    <span class="member-name">{{ member.full_name }}</span>
                    <span class="member-position">{{ member.position }}</span>
                  </span>
                </label>
              </div>
            </div>

            <p v-if="allMembers.length === 0" class="no-data-small">Нет доступных участников</p>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить изменения</button>
            <button type="button" @click="$router.push('/crews')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getCrewDetails, updateCrew, getCrewMembers } from '../api/index.js';

export default {
  name: 'EditCrew',
  data() {
    return {
      crew: {
        id: null,
      },
      allMembers: [],
      selectedMemberIds: [],
      error: null,
    };
  },
  async created() {
    const crewId = this.$route.params.id;
    try {
      const [crewResponse, membersResponse] = await Promise.all([
        getCrewDetails(crewId),
        getCrewMembers(),
      ]);

      this.crew = crewResponse.data;
      this.allMembers = membersResponse.data;

      this.selectedMemberIds = this. crew.members.map((member) => member.id);
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const crewId = this.$route.params.id;
      try {
        const updatedCrewData = {
          id: crewId,
          member_ids: this.selectedMemberIds,
        };
        await updateCrew(crewId, updatedCrewData);
        alert('Команда успешно обновлена.');
        this.$router.push('/crews');
      } catch (err) {
        alert('Ошибка сохранения изменений.');
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.edit-crew {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color:  #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 30px;
}

.form-section h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 20px;
}

.section-description {
  margin-bottom: 20px;
  color: #666;
  font-size: 14px;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  overflow-y:  auto;
  padding:  15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.member-checkbox {
  background-color: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 12px 15px;
  transition: all 0.2s ease;
}

.member-checkbox:hover {
  background-color: #f8f9fa;
  border-color: #007BFF;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  margin:  0;
  font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
  width:  18px;
  height:  18px;
  margin-right: 12px;
  cursor: pointer;
  accent-color: #007BFF;
  flex-shrink: 0;
}

.member-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-name {
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.member-position {
  color: #666;
  font-size: 13px;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.button-group.button {
  flex: 1;
}

.no-data-small {
  color: #666;
  font-style: italic;
  margin:  0;
  padding: 20px;
  text-align: center;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .members-list {
    max-height: 300px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>