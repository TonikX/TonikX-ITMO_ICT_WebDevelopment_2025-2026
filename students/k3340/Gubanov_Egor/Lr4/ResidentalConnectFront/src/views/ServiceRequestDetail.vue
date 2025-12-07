<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card v-if="request">
          <v-card-title class="d-flex align-center">
            <span>Заявка #{{ request.id }}</span>
            <v-spacer></v-spacer>
            <StatusChip :status="request.status" />
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-card variant="outlined" class="mb-4">
                  <v-card-title>Основная информация</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item>
                        <v-list-item-title>Тема</v-list-item-title>
                        <v-list-item-subtitle>{{ request.title }}</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Описание</v-list-item-title>
                        <v-list-item-subtitle>{{ request.description }}</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Категория</v-list-item-title>
                        <v-list-item-subtitle>{{ request.category?.name || '-' }}</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Квартира</v-list-item-title>
                        <v-list-item-subtitle>
                          {{ request.apartment ? `Кв. ${request.apartment.number}, ${request.apartment.building?.address}` : '-' }}
                        </v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Приоритет</v-list-item-title>
                        <v-list-item-subtitle>
                          <PriorityChip :priority="request.priority" />
                        </v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Заявитель</v-list-item-title>
                        <v-list-item-subtitle>
                          {{ request.requester?.first_name }} {{ request.requester?.last_name }} ({{ request.requester?.username }})
                        </v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item v-if="request.worker">
                        <v-list-item-title>Мастер</v-list-item-title>
                        <v-list-item-subtitle>
                          {{ request.worker?.first_name }} {{ request.worker?.last_name }} ({{ request.worker?.username }})
                        </v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Дата создания</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDateTime(request.created_at) }}</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item v-if="request.resolved_at">
                        <v-list-item-title>Дата решения</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDateTime(request.resolved_at) }}</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Комментарий мастера -->
              <v-col cols="12" v-if="request.worker_comment">
                <v-card variant="outlined" class="mb-4">
                  <v-card-title>Комментарий мастера</v-card-title>
                  <v-card-text>
                    {{ request.worker_comment }}
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Действия для мастера/диспетчера -->
              <v-col cols="12" v-if="canManage">
                <v-card variant="outlined">
                  <v-card-title>Управление заявкой</v-card-title>
                  <v-card-text>
                    <v-row>
                      <!-- Назначение мастера (только для диспетчера) -->
                      <v-col cols="12" v-if="userIsDispatcher && !request.worker">
                        <WorkerSelect
                          v-model="workerId"
                          label="Назначить мастера"
                        />
                        <v-btn
                          color="primary"
                          class="mt-2"
                          @click="assignWorker"
                          :loading="loading"
                        >
                          Назначить
                        </v-btn>
                      </v-col>

                      <!-- Изменение статуса -->
                      <v-col cols="12" v-if="canChangeStatus">
                        <v-select
                          v-model="newStatus"
                          :items="statusOptions"
                          label="Изменить статус"
                          variant="outlined"
                        ></v-select>
                        <v-btn
                          color="primary"
                          class="mt-2"
                          @click="changeStatus"
                          :loading="loading"
                        >
                          Изменить статус
                        </v-btn>
                      </v-col>

                      <!-- Добавление комментария -->
                      <v-col cols="12" v-if="canAddComment">
                        <v-textarea
                          v-model="comment"
                          label="Комментарий мастера"
                          variant="outlined"
                          rows="3"
                        ></v-textarea>
                        <v-btn
                          color="primary"
                          class="mt-2"
                          @click="addComment"
                          :loading="loading"
                        >
                          Добавить комментарий
                        </v-btn>
                      </v-col>

                      <!-- Редактирование -->
                      <v-col cols="12" v-if="canEdit">
                        <v-btn
                          color="primary"
                          prepend-icon="mdi-pencil"
                          @click="$router.push(`/service-requests/${request.id}/edit`)"
                        >
                          Редактировать
                        </v-btn>
                      </v-col>

                      <!-- Удаление -->
                      <v-col cols="12" v-if="canDelete">
                        <v-btn
                          color="error"
                          prepend-icon="mdi-delete"
                          @click="confirmDelete"
                        >
                          Удалить
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-card v-else-if="loading">
          <v-card-text>
            <v-skeleton-loader type="card"></v-skeleton-loader>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить эту заявку?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" @click="deleteRequest">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { serviceRequestsService } from '@/services/serviceRequestsService'
import { useAuthStore } from '@/stores/auth'
import { isResident, isMaster, isDispatcher } from '@/utils/roleUtils'
import { formatDateTime } from '@/utils/dateUtils'
import { getRequestStatusOptions, REQUEST_STATUSES } from '@/utils/statusUtils'
import StatusChip from '@/components/StatusChip.vue'
import PriorityChip from '@/components/PriorityChip.vue'
import WorkerSelect from '@/components/WorkerSelect.vue'

export default {
  name: 'ServiceRequestDetail',
  components: {
    StatusChip,
    PriorityChip,
    WorkerSelect,
  },
  data() {
    return {
      request: null,
      loading: false,
      workerId: null,
      newStatus: null,
      comment: '',
      deleteDialog: false,
      statusOptions: getRequestStatusOptions(),
    }
  },
  computed: {
    user() {
      return useAuthStore().user
    },
    userIsDispatcher() {
      return isDispatcher(this.user)
    },
    userIsMaster() {
      return isMaster(this.user)
    },
    canManage() {
      return this.userIsDispatcher || (this.userIsMaster && this.request?.worker?.id === this.user?.id)
    },
    canChangeStatus() {
      return this.canManage && this.request?.status !== REQUEST_STATUSES.CANCELED
    },
    canAddComment() {
      return this.canManage
    },
    canEdit() {
      return this.isDispatcher || (this.request?.requester?.id === this.user?.id)
    },
    canDelete() {
      return this.canEdit
    },
  },
  async mounted() {
    await this.loadRequest()
  },
  methods: {
    async loadRequest() {
      this.loading = true
      try {
        this.request = await serviceRequestsService.getServiceRequest(this.$route.params.id)
      } catch (error) {
        console.error('Error loading request:', error)
        this.$router.push('/service-requests')
      } finally {
        this.loading = false
      }
    },
    async assignWorker() {
      if (!this.workerId) return
      this.loading = true
      try {
        await serviceRequestsService.assignWorker(this.request.id, this.workerId)
        await this.loadRequest()
        this.workerId = null
      } catch (error) {
        console.error('Error assigning worker:', error)
      } finally {
        this.loading = false
      }
    },
    async changeStatus() {
      if (!this.newStatus) return
      this.loading = true
      try {
        await serviceRequestsService.changeStatus(this.request.id, this.newStatus)
        await this.loadRequest()
        this.newStatus = null
      } catch (error) {
        console.error('Error changing status:', error)
      } finally {
        this.loading = false
      }
    },
    async addComment() {
      if (!this.comment.trim()) return
      this.loading = true
      try {
        await serviceRequestsService.addComment(this.request.id, this.comment)
        await this.loadRequest()
        this.comment = ''
      } catch (error) {
        console.error('Error adding comment:', error)
      } finally {
        this.loading = false
      }
    },
    confirmDelete() {
      this.deleteDialog = true
    },
    async deleteRequest() {
      this.loading = true
      try {
        await serviceRequestsService.deleteServiceRequest(this.request.id)
        this.$router.push('/service-requests')
      } catch (error) {
        console.error('Error deleting request:', error)
      } finally {
        this.loading = false
        this.deleteDialog = false
      }
    },
    formatDateTime,
  },
}
</script>

