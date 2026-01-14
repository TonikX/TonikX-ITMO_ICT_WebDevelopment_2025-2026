<template>
  <div>
    <div class="header-row">
      <button class="btn-back" @click="$router.back()">← Back</button>
      <h2 class="h1">{{ isNew ? 'Create owner' : 'Edit owner' }}</h2>
      <div><button class="btn" @click="save">Save</button></div>
    </div>

    <div class="card">
      <div class="form-row">
        <div class="form-control">
          <label>First name</label>
          <input class="input" v-model="form.first_name" />
        </div>
        <div class="form-control">
          <label>Last name</label>
          <input class="input" v-model="form.last_name" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-control">
          <label>City</label>
          <input class="input" v-model="form.city" />
        </div>
        <div class="form-control">
          <label>Date of birth</label>
          <input type="date" class="input" v-model="form.date_of_birth" />
        </div>
      </div>

      <div style="margin-top:12px;">
        <button class="btn" @click="save">Save</button>
        <button class="btn secondary" @click="$router.back()">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
export default {
  props: ["id"],
  data(){ return {
    form: { first_name: '', last_name: '', city: '', date_of_birth: null },
    loading: false
  }},
  computed: { isNew(){ return this.id === 'new' || this.$route.params.id === 'new'; } },
  async created(){
    const id = this.id || this.$route.params.id;
    if(!this.isNew) {
      try {
        const res = await api.get(`api/owners/${id}/`);
        this.form = { ...res.data };
      } catch(e){ console.error(e); }
    }
  },
  methods:{
    async save(){
      this.loading = true;
      try {
        if(this.isNew) {
          await api.post('api/owners/', this.form);
        } else {
          await api.put(`api/owners/${this.form.id}/`, this.form);
        }
        this.$router.push({ name: 'Owners' });
      } catch(e){
        console.error(e);
        alert('Save failed');
      } finally { this.loading = false; }
    }
  }
}
</script>