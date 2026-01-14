<template>
  <div>
    <div class="header-row">
      <h1 class="h1">Owners</h1>
      <div>
        <button class="btn" @click="refresh">Refresh</button>
        <button class="btn secondary" @click="createOwner">Add owner</button>
      </div>
    </div>

    <div class="card">
      <div v-if="loading" style="padding:24px;">
        <LoadingSpinner />
      </div>
      <div v-else>
        <ul class="list">
          <li v-for="o in owners" :key="o.id" class="list-item">
            <div>
              <router-link :to="{ name: 'OwnerDetail', params: { id: o.id } }">
                <strong>{{ o.last_name }} {{ o.first_name }}</strong>
              </router-link>
              <div class="small">{{ o.city || '—' }}</div>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
              <router-link :to="{ name: 'OwnerDetail', params: { id: o.id } }" class="small">View</router-link>
              <router-link :to="{ name: 'OwnerEdit', params: { id: o.id } }" class="small">Edit</router-link>
            </div>
          </li>
        </ul>

        <EmptyState v-if="owners.length === 0">No owners yet. Click "Add owner" to create one.</EmptyState>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import EmptyState from "@/components/EmptyState.vue";

export default {
  components: { LoadingSpinner, EmptyState },
  data(){ return { owners: [], loading: true } },
  async created(){ await this.fetch(); },
  methods:{
    async fetch(){
      this.loading = true;
      try {
        const res = await api.get("api/owners/");
        this.owners = res.data.results || res.data;
      } catch(e){ console.error(e); }
      finally{ this.loading = false; }
    },
    refresh(){ this.fetch(); },
    createOwner(){ this.$router.push({ name: 'OwnerEdit', params: { id: 'new' } }); }
  }
}
</script>