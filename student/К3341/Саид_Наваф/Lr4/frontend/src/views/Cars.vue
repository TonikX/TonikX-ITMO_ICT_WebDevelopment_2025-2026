<template>
  <div>
    <div class="header-row">
      <h1 class="h1">Cars</h1>
      <div>
        <button class="btn" @click="refresh">Refresh</button>
        <button class="btn secondary" @click="showCreateModal = true">Add car</button>
      </div>
    </div>

    <div class="card">
      <div v-if="loading" style="padding:24px;">
        <LoadingSpinner />
      </div>
      <div v-else>
        <ul class="list">
          <li v-for="c in cars" :key="c.id" class="list-item">
            <div>
              <router-link :to="{ name: 'CarDetail', params: { id: c.id } }">
                <strong>{{ c.vehicle_model?.manufacturer || '' }} {{ c.vehicle_model?.model || '' }}</strong>
              </router-link>
              <div class="small">VIN: {{ c.vin }}</div>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
              <router-link :to="{ name: 'CarDetail', params: { id: c.id } }" class="small">View</router-link>
            </div>
          </li>
        </ul>

        <EmptyState v-if="cars.length === 0">No cars found.</EmptyState>
      </div>
    </div>

    <!-- Create Car Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h2>Add New Car</h2>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="submitCar">
            <div class="form-group">
              <label for="vin">VIN (Vehicle Identification Number) *</label>
              <input 
                type="text" 
                id="vin" 
                v-model="newCar.vin" 
                required
                maxlength="17"
                placeholder="Enter 17-character VIN"
                :class="{ 'error': errors.vin }"
              />
              <div v-if="errors.vin" class="error-message">{{ errors.vin }}</div>
            </div>

            <div class="form-group">
              <label for="manufacturer">Manufacturer *</label>
              <input 
                type="text" 
                id="manufacturer" 
                v-model="newCar.manufacturer" 
                required
                placeholder="e.g., Toyota, Ford, BMW"
                :class="{ 'error': errors.manufacturer }"
              />
              <div v-if="errors.manufacturer" class="error-message">{{ errors.manufacturer }}</div>
            </div>

            <div class="form-group">
              <label for="model">Model *</label>
              <input 
                type="text" 
                id="model" 
                v-model="newCar.model" 
                required
                placeholder="e.g., Camry, F-150, 3 Series"
                :class="{ 'error': errors.model }"
              />
              <div v-if="errors.model" class="error-message">{{ errors.model }}</div>
            </div>

            <div class="form-group">
              <label for="year">Year *</label>
              <input 
                type="number" 
                id="year" 
                v-model="newCar.year" 
                required
                min="1900"
                :max="new Date().getFullYear() + 1"
                placeholder="e.g., 2023"
                :class="{ 'error': errors.year }"
              />
              <div v-if="errors.year" class="error-message">{{ errors.year }}</div>
            </div>

            <div class="form-group">
              <label for="color">Color</label>
              <input 
                type="text" 
                id="color" 
                v-model="newCar.color" 
                placeholder="e.g., Red, Blue, Black"
              />
            </div>

            <div class="form-group">
              <label for="mileage">Mileage</label>
              <input 
                type="number" 
                id="mileage" 
                v-model="newCar.mileage" 
                min="0"
                placeholder="Current mileage"
              />
            </div>

            <div class="form-actions">
              <button 
                type="button" 
                class="btn secondary" 
                @click="closeModal"
                :disabled="isSubmitting"
              >
                Cancel
              </button>
              <button 
                type="submit" 
                class="btn" 
                :disabled="isSubmitting"
              >
                <span v-if="isSubmitting">Adding...</span>
                <span v-else>Add Car</span>
              </button>
            </div>
          </form>
        </div>
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
  data() { 
    return { 
      cars: [], 
      loading: true,
      showCreateModal: false,
      isSubmitting: false,
      newCar: {
        vin: '',
        manufacturer: '',
        model: '',
        year: '',
        color: '',
        mileage: ''
      },
      errors: {}
    } 
  },
  async created(){ 
    await this.fetch(); 
  },
  methods: {
    async fetch(){
      this.loading = true;
      try {
        const res = await api.get("api/cars/");
        this.cars = res.data.results || res.data;
      } catch(e){ 
        console.error("Error fetching cars:", e);
        // Optional: Add toast notification
      }
      finally{ this.loading = false; }
    },
    
    refresh(){ 
      this.fetch(); 
    },
    
    closeModal() {
      if (!this.isSubmitting) {
        this.showCreateModal = false;
        this.resetForm();
      }
    },
    
    resetForm() {
      this.newCar = {
        vin: '',
        manufacturer: '',
        model: '',
        year: '',
        color: '',
        mileage: ''
      };
      this.errors = {};
    },
    
    validateForm() {
      this.errors = {};
      let isValid = true;
      
      // VIN validation (standard VIN is 17 characters)
      if (!this.newCar.vin) {
        this.errors.vin = 'VIN is required';
        isValid = false;
      } else if (this.newCar.vin.length !== 17) {
        this.errors.vin = 'VIN must be 17 characters';
        isValid = false;
      }
      
      if (!this.newCar.manufacturer) {
        this.errors.manufacturer = 'Manufacturer is required';
        isValid = false;
      }
      
      if (!this.newCar.model) {
        this.errors.model = 'Model is required';
        isValid = false;
      }
      
      if (!this.newCar.year) {
        this.errors.year = 'Year is required';
        isValid = false;
      } else if (this.newCar.year < 1900 || this.newCar.year > new Date().getFullYear() + 1) {
        this.errors.year = 'Please enter a valid year';
        isValid = false;
      }
      
      return isValid;
    },
    
    async submitCar() {
      if (!this.validateForm()) {
        return;
      }
      
      this.isSubmitting = true;
      
      try {
        // Format the data according to your API structure
        const carData = {
          vin: this.newCar.vin.toUpperCase(), // VINs are typically uppercase
          vehicle_model: {
            manufacturer: this.newCar.manufacturer,
            model: this.newCar.model,
            year: parseInt(this.newCar.year)
          },
          ...(this.newCar.color && { color: this.newCar.color }),
          ...(this.newCar.mileage && { mileage: parseInt(this.newCar.mileage) })
        };
        
        const response = await api.post("api/cars/", carData);
        
        // Add the new car to the list and close modal
        this.cars.unshift(response.data);
        this.closeModal();
        
        // Optional: Show success message
        // this.$toast.success('Car added successfully!');
        
      } catch (error) {
        console.error("Error creating car:", error);
        
        // Handle API validation errors
        if (error.response && error.response.data) {
          // You can map API errors to form fields
          const apiErrors = error.response.data;
          
          // Example: Handle different error structures
          if (apiErrors.vin) {
            this.errors.vin = Array.isArray(apiErrors.vin) ? apiErrors.vin[0] : apiErrors.vin;
          }
          
          // Add a generic error message
          if (!this.errors.vin && error.response.data.detail) {
            // this.$toast.error(error.response.data.detail);
          }
        } else {
          // this.$toast.error('Failed to add car. Please try again.');
        }
      } finally {
        this.isSubmitting = false;
      }
    }
  }
}
</script>

<style scoped>
/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e5e5;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  color: #333;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.modal-body {
  padding: 24px;
}

/* Form Styles */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.form-group input.error {
  border-color: #e74c3c;
}

.error-message {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e5e5e5;
}

/* Responsive */
@media (max-width: 600px) {
  .modal {
    width: 95%;
    margin: 10px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions button {
    width: 100%;
  }
}
</style>