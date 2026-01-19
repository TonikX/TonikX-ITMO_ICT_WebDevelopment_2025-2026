<template>
  <v-card>
    <v-card-title>
      Service Contracts
      <v-spacer></v-spacer>
      <v-btn @click="showCreateModal = true">+ Add Contract</v-btn>
    </v-card-title>

    <div v-if="loading" class="text-center pa-4">Loading contracts...</div>

    <div v-else>
      <div class="d-flex justify-space-between pa-4">
        <div>
          <div>Total Contracts: {{ count }}</div>
          <div>Active Contracts: {{ activeContractsCount }}</div>
          <div>
            Object Status:
            <v-chip :color="objectIsServiced ? 'green' : 'grey'">
              {{ objectIsServiced ? "Under Service" : "Not Serviced" }}
            </v-chip>
          </div>
        </div>
      </div>

      <v-table v-if="contracts.length">
        <thead>
          <tr>
            <th>Contract #</th>
            <th>Enterprise</th>
            <th>Contract Date</th>
            <th>Status</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contract in contracts" :key="contract.id">
            <td>{{ contract.contract_number }}</td>
            <td>
              <div v-if="contract.enterprise">
                <strong>{{ contract.enterprise.name }}</strong>
                <div>{{ contract.enterprise.legal_address }}</div>
              </div>
              <div v-else>Enterprise not found</div>
            </td>
            <td>{{ formatDate(contract.contract_date) }}</td>
            <td>
              <v-chip :color="contract.is_active ? 'green' : 'grey'">
                {{ contract.is_active ? "Active" : "Inactive" }}
              </v-chip>
            </td>
            <td>{{ contract.description || "-" }}</td>
            <td>
              <v-btn @click="editContract(contract)" size="small" class="mr-2">
                Edit
              </v-btn>
              <v-btn
                @click="handleDeleteContract(contract.id)"
                color="error"
                size="small"
              >
                Delete
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>

      <div v-else class="text-center pa-4">No contracts found</div>

      <div v-if="count > 0" class="d-flex justify-center pa-4">
        <v-btn @click="prevPage" :disabled="!previous">Previous</v-btn>
        <span class="mx-4">Page {{ page }} of {{ totalPages }}</span>
        <v-btn @click="nextPage" :disabled="!next">Next</v-btn>
      </div>
    </div>

    <v-dialog v-model="showDialog" width="500">
      <v-card>
        <v-card-title>
          {{ editingContract ? "Edit Contract" : "Add New Contract" }}
        </v-card-title>
        <v-form @submit.prevent="saveContract" class="pa-4">
          <v-text-field
            v-model="contractForm.contract_number"
            label="Contract Number"
            required
          ></v-text-field>

          <v-select
            v-model="contractForm.enterprise"
            :items="enterprises"
            item-title="name"
            item-value="id"
            label="Enterprise"
            required
            :loading="loadingEnterprises"
          ></v-select>

          <v-text-field
            v-model="contractForm.contract_date"
            type="date"
            label="Contract Date"
            required
          ></v-text-field>

          <v-textarea
            v-model="contractForm.description"
            label="Description"
            rows="3"
          ></v-textarea>

          <v-checkbox
            v-model="contractForm.is_active"
            label="Active Contract"
          ></v-checkbox>

          <div class="d-flex justify-space-between">
            <v-btn @click="closeModal">Cancel</v-btn>
            <v-btn type="submit" color="primary" :loading="saving">Save</v-btn>
          </div>
        </v-form>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref, onMounted, computed, reactive, watch } from "vue";
import { useAuthStore } from "@/store/auth";
import {
  getContractsByObject,
  createContract,
  updateContract,
  deleteContract as deleteContractApi,
} from "@/services/contractsService";
import { getEnterprises } from "@/services/enterprisesService";

const props = defineProps({
  objectId: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["contractUpdated"]);
const auth = useAuthStore();

const loading = ref(true);
const saving = ref(false);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const loadingEnterprises = ref(false);

const contracts = ref([]);
const count = ref(0);
const next = ref(null);
const previous = ref(null);
const page = ref(1);
const pageSize = ref(10);

const enterprises = ref([]);
const editingContract = ref(null);

const contractForm = reactive({
  contract_number: "",
  enterprise: null,
  contract_date: "",
  description: "",
  is_active: true,
});

const showDialog = computed({
  get() {
    return showCreateModal.value || showEditModal.value;
  },
  set(value) {
    if (!value) {
      showCreateModal.value = false;
      showEditModal.value = false;
    }
  },
});

const totalPages = computed(() => Math.ceil(count.value / pageSize.value));

const activeContractsCount = computed(() => {
  return contracts.value.filter((c) => c.is_active).length;
});

const objectIsServiced = computed(() => {
  return activeContractsCount.value > 0;
});

const loadContracts = async () => {
  try {
    loading.value = true;
    const data = await getContractsByObject(
      props.objectId,
      auth.token,
      page.value
    );
    contracts.value = data.results || data || [];
    count.value = data.count || contracts.value.length;
    next.value = data.next;
    previous.value = data.previous;
  } catch (error) {
    console.error("Error loading contracts:", error);
    contracts.value = [];
    count.value = 0;
  } finally {
    loading.value = false;
  }
};

const loadEnterprises = async () => {
  try {
    loadingEnterprises.value = true;
    const data = await getEnterprises(auth.token);
    enterprises.value = data.results || data || [];
  } catch (error) {
    console.error("Error loading enterprises:", error);
    enterprises.value = [];
  } finally {
    loadingEnterprises.value = false;
  }
};

const nextPage = () => {
  if (next.value) {
    page.value++;
  }
};

const prevPage = () => {
  if (previous.value) {
    page.value--;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "-";
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  } catch (e) {
    return dateString;
  }
};

const editContract = (contract) => {
  editingContract.value = contract;
  Object.assign(contractForm, {
    contract_number: contract.contract_number,
    enterprise: contract.enterprise?.id || "",
    contract_date: contract.contract_date,
    description: contract.description || "",
    is_active: contract.is_active,
  });
  showEditModal.value = true;
};

const saveContract = async () => {
  saving.value = true;
  try {
    if (!contractForm.enterprise || contractForm.enterprise === "") {
      alert("Please select an enterprise");
      saving.value = false;
      return;
    }

    const contractData = {
      contract_number: contractForm.contract_number,
      enterprise: parseInt(contractForm.enterprise),
      object: parseInt(props.objectId),
      contract_date: contractForm.contract_date,
      description: contractForm.description,
      is_active: contractForm.is_active,
    };

    let response;
    if (editingContract.value) {
      response = await updateContract(
        editingContract.value.id,
        contractData,
        auth.token
      );
    } else {
      response = await createContract(contractData, auth.token);
    }

    await loadContracts();
    closeModal();
    emit("contractUpdated");
  } catch (error) {
    console.error("Error saving contract:", error);
    alert("Failed to save contract");
  } finally {
    saving.value = false;
  }
};

const handleDeleteContract = async (contractId) => {
  if (!confirm("Are you sure you want to delete this contract?")) return;

  try {
    await deleteContractApi(contractId, auth.token);
    await loadContracts();
    emit("contractUpdated");
  } catch (error) {
    console.error("Error deleting contract:", error);
    alert("Failed to delete contract");
  }
};

const closeModal = () => {
  showCreateModal.value = false;
  showEditModal.value = false;
  editingContract.value = null;
  Object.assign(contractForm, {
    contract_number: "",
    enterprise: "",
    contract_date: "",
    description: "",
    is_active: true,
  });
};

onMounted(async () => {
  await Promise.all([loadContracts(), loadEnterprises()]);
});

watch(page, () => {
  loadContracts();
});

watch(
  () => props.objectId,
  () => {
    page.value = 1;
    loadContracts();
  }
);
</script>
