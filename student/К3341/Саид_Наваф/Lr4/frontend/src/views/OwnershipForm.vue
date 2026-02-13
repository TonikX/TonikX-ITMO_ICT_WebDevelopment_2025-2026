<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal">
      <h3>Create ownership</h3>
      <div class="form-row">
        <div class="form-control">
          <label>Car</label>
          <select v-model="form.car" class="input">
            <option v-for="c in cars" :key="c.id" :value="c.id">{{ c.vin }} — {{ c.vehicle_model?.manufacturer }} {{ c.vehicle_model?.model }}</option>
          </select>
        </div>
        <div class="form-control">
          <label>Start date</label>
          <input type="date" v-model="form.date_start" class="input" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-control">
          <label>End date</label>
          <input type="date" v-model="form.date_end" class="input" />
        </div>
        <div class="form-control">
          <label>Notes</label>
          <input class="input" v-model="form.notes" />
        </div>
      </div>

      <div style="display:flex; gap:8px; justify-content:flex-end;">
        <button class="btn secondary" @click="$emit('close')">Cancel</button>
        <button class="btn" @click="create">Create</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
export default {
  props: { ownerId: { required: true } },
  data(){ return { cars: [], form: { car: null, date_start: '', date_end: '', notes: '' } } },
  async created(){
    const res = await api.get('api/cars/');
    this.cars = res.data.results || res.data;
    if(this.cars.length) this.form.car = this.cars[0].id;
  },
  methods:{
    async create(){
      try {
        await api.post('api/ownerships/', { owner: this.ownerId, car: this.form.car, date_start: this.form.date_start, date_end: this.form.date_end, notes: this.form.notes });
        this.$emit('created');
        this.$emit('close');
      } catch(e){ console.error(e); alert('Failed to create'); }
    }
  }
}
</script>