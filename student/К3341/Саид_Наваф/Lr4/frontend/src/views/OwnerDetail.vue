<template>
  <div class="container">
    <div class="card">
      <div class="header-row">
        <div>
          <button class="btn-back" @click="$router.back()">← Back</button>
        </div>
        <div>
          <h2 class="h1">{{ owner?.last_name }} {{ owner?.first_name }}</h2>
          <div class="small">ID: {{ owner?.id }} • {{ owner?.created_at | shortDate }}</div>
        </div>
        <div>
          <button class="btn" @click="refresh">Refresh</button>
        </div>
      </div>

      <div class="grid-2">
        <div>
          <div class="section-title">Personal</div>
          <div class="card" style="padding:12px;">
            <div class="kv"><b>Name</b> {{ owner?.first_name }} {{ owner?.last_name }}</div>
            <div class="kv"><b>City</b> <span class="small">{{ owner?.city || '-' }}</span></div>
            <div class="kv"><b>DOB</b> <span class="small">{{ owner?.date_of_birth || '-' }}</span></div>
          </div>

          <div class="section-title">Driver license</div>
          <div class="card" style="padding:12px;">
            <div v-if="owner?.driver_license">
              <div class="kv"><b>Number</b> {{ owner.driver_license.license_number }}</div>
              <div class="kv"><b>Issue date</b> {{ owner.driver_license.issue_date }}</div>
              <div class="kv"><b>Type</b> <span class="badge secondary">{{ owner.driver_license.license_type || '—' }}</span></div>
            </div>
            <div v-else class="empty">No driver license recorded</div>
          </div>

          <div class="section-title">Contacts</div>
          <ul class="list">
            <li v-for="c in owner.contacts || []" :key="c.id" class="list-item">
              <div>
                <div><strong>{{ c.type }}</strong> — {{ c.value }}</div>
                <div class="small" v-if="c.is_primary">Primary</div>
              </div>
              <div class="meta">ID: {{ c.id }}</div>
            </li>
            <li v-if="!(owner.contacts && owner.contacts.length)" class="empty">No contacts</li>
          </ul>
        </div>

        <div>
          <div class="section-title">Ownerships</div>
          <div class="card" style="padding:12px;">
            <ul class="list">
              <li v-for="ow in owner.ownerships || []" :key="ow.id" class="list-item">
                <div>
                  <router-link :to="{ name: 'CarDetail', params: { id: ow.car.id } }">
                    <strong>{{ ow.car.vehicle_model?.manufacturer }} {{ ow.car.vehicle_model?.model }}</strong>
                  </router-link>
                  <div class="small">VIN: {{ ow.car.vin }}</div>
                  <div class="small">Period: {{ ow.date_start }} — {{ ow.date_end || 'present' }}</div>
                  <div v-if="ow.notes" class="small">Notes: {{ ow.notes }}</div>
                </div>
                <div class="meta">OwID: {{ ow.id }}</div>
              </li>
              <li v-if="!(owner.ownerships && owner.ownerships.length)" class="empty">No ownership records</li>
            </ul>
          </div>

          <div class="section-title">Quick actions</div>
          <div style="display:flex; gap:8px;">
            <button class="btn" @click="goEdit">Edit owner</button>
            <button class="btn secondary" @click="createOwnership">Add ownership</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
export default {
  name: "OwnerDetail",
  props: ["id"],
  data(){ return { owner: null, loading: true } },
  async created(){
    await this.fetchOwner();
  },
  methods: {
    async fetchOwner(){
      this.loading = true;
      const id = this.id || this.$route.params.id;
      try {
        const res = await api.get(`api/owners/${id}/`);
        this.owner = res.data;
      } catch(e){
        console.error(e);
      } finally { this.loading = false; }
    },
    refresh(){ this.fetchOwner(); },
    goEdit(){ this.$router.push({ name: 'OwnerEdit', params: { id: this.owner.id } }).catch(()=>{}); },
    createOwnership(){ alert('Open create ownership dialog (not implemented)'); }
  },
  filters: {
    shortDate(val){ if(!val) return '-'; return val.split('T')[0]; }
  }
}
</script>