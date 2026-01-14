<template>
  <div class="container">
    <div class="card">
      <div class="header-row">
        <div>
          <button class="btn-back" @click="$router.back()">← Back</button>
        </div>
        <div>
          <h2 class="h1">{{ car?.vehicle_model?.manufacturer }} {{ car?.vehicle_model?.model }}</h2>
          <div class="small">VIN: {{ car?.vin }} • ID: {{ car?.id }}</div>
        </div>
        <div>
          <button class="btn" @click="refresh">Refresh</button>
        </div>
      </div>

      <div class="grid-2">
        <div>
          <div class="section-title">Main info</div>
          <div class="card" style="padding:12px;">
            <div class="kv"><b>VIN</b> {{ car?.vin }}</div>
            <div class="kv"><b>Reg. number</b> {{ car?.registration_number || '-' }}</div>
            <div class="kv"><b>Color</b> {{ car?.color || '-' }}</div>
            <div class="kv"><b>Year</b> {{ car?.year || '-' }}</div>
          </div>

          <div class="section-title">Insurance policies</div>
          <ul class="list">
            <li v-for="p in policies" :key="p.id" class="list-item">
              <div>
                <div><strong>{{ p.policy_number }}</strong> — {{ p.insurer }}</div>
                <div class="small">{{ p.date_start }} — {{ p.date_end || 'present' }}</div>
              </div>
              <div class="meta">ID: {{ p.id }}</div>
            </li>
            <li v-if="policies.length === 0" class="empty">No active policies</li>
          </ul>
        </div>

        <div>
          <div class="section-title">Service & Registration</div>
          <div class="card" style="padding:12px;">
            <div class="section-title">Service records</div>
            <ul class="list">
              <li v-for="s in services" :key="s.id" class="list-item">
                <div>
                  <div><strong>{{ s.date }}</strong> — {{ s.mileage || '—' }} km</div>
                  <div class="small">{{ s.description }}</div>
                </div>
                <div class="meta">ID: {{ s.id }}</div>
              </li>
              <li v-if="services.length === 0" class="empty">No service history</li>
            </ul>

            <div class="section-title" style="margin-top:12px;">Registrations</div>
            <ul class="list">
              <li v-for="r in registrations" :key="r.id" class="list-item">
                <div>
                  <div><strong>{{ r.reg_number }}</strong></div>
                  <div class="small">Valid: {{ r.valid_from }} — {{ r.valid_to || '—' }}</div>
                </div>
                <div class="meta">ID: {{ r.id }}</div>
              </li>
              <li v-if="registrations.length === 0" class="empty">No registration info</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
export default {
  name: "CarDetail",
  props: ["id"],
  data(){ return { car:null, policies:[], services:[], registrations:[], loading:true } },
  async created(){ await this.fetchAll(); },
  methods:{
    async fetchAll(){
      this.loading = true;
      const id = this.id || this.$route.params.id;
      try{
        const res = await api.get(`api/cars/${id}/`);
        this.car = res.data;
        const p = await api.get(`api/insurance/?car=${id}`);
        this.policies = p.data.results || p.data;
        const s = await api.get(`api/services/?car=${id}`);
        this.services = s.data.results || s.data;
        const r = await api.get(`api/registrations/?car=${id}`);
        this.registrations = r.data.results || r.data;
      }catch(e){ console.error(e); }
      finally{ this.loading = false; }
    },
    refresh(){ this.fetchAll(); }
  }
}
</script>