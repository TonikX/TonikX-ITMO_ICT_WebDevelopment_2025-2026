<template>
  <v-container>
    <div class="mb-4">
      <v-btn @click="router.push('/dashboard')" prepend-icon="mdi-arrow-left">
        Back to Dashboard
      </v-btn>
    </div>

    <v-card>
      <v-card-title>Account Settings</v-card-title>

      <v-tabs v-model="activeTab" class="mb-4">
        <v-tab value="profile">Profile</v-tab>
        <v-tab value="password">Password</v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <v-window-item value="profile">
          <v-form @submit.prevent="updateProfile" class="pa-4">
            <v-text-field
              v-model="profileForm.username"
              label="Username"
              required
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model="profileForm.email"
              label="Email"
              type="email"
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model="profileForm.first_name"
              label="First Name"
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model="profileForm.last_name"
              label="Last Name"
              class="mb-3"
            ></v-text-field>

            <div class="d-flex justify-space-between">
              <v-btn @click="resetProfileForm" :disabled="updatingProfile">
                Reset
              </v-btn>
              <v-btn type="submit" color="primary" :loading="updatingProfile">
                Save Changes
              </v-btn>
            </div>
          </v-form>
        </v-window-item>

        <v-window-item value="password">
          <v-form @submit.prevent="changeUserPassword" class="pa-4">
            <v-text-field
              v-model="passwordForm.current_password"
              label="Current Password"
              type="password"
              required
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model="passwordForm.new_password"
              label="New Password"
              type="password"
              required
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model="passwordForm.confirm_password"
              label="Confirm Password"
              type="password"
              required
              class="mb-3"
            ></v-text-field>

            <div class="d-flex justify-space-between">
              <v-btn @click="resetPasswordForm" :disabled="changingPassword">
                Clear
              </v-btn>
              <v-btn type="submit" color="primary" :loading="changingPassword">
                Change Password
              </v-btn>
            </div>
          </v-form>
        </v-window-item>
      </v-window>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { updateUser, changePassword } from "@/services/authService";

const router = useRouter();
const authStore = useAuthStore();

const activeTab = ref("profile");

const profileForm = reactive({
  username: "",
  email: "",
  first_name: "",
  last_name: "",
});

const originalProfile = ref({});
const updatingProfile = ref(false);

const passwordForm = reactive({
  current_password: "",
  new_password: "",
  confirm_password: "",
});

const changingPassword = ref(false);

const loadUserData = () => {
  const user = authStore.user;
  if (user) {
    profileForm.username = user.username || "";
    profileForm.email = user.email || "";
    profileForm.first_name = user.first_name || "";
    profileForm.last_name = user.last_name || "";
    originalProfile.value = { ...profileForm };
  }
};

const updateProfile = async () => {
  updatingProfile.value = true;

  try {
    if (!profileForm.username.trim()) {
      alert("Username is required");
      return;
    }

    const updatedUser = await updateUser(
      authStore.user.id,
      {
        username: profileForm.username,
        email: profileForm.email || "",
        first_name: profileForm.first_name || "",
        last_name: profileForm.last_name || "",
      },
      authStore.token
    );

    authStore.setUser(updatedUser);
    originalProfile.value = { ...profileForm };
    alert("Profile updated successfully!");
  } catch (error) {
    alert(`Update failed: ${error.response?.data?.detail || error.message}`);
  } finally {
    updatingProfile.value = false;
  }
};

const changeUserPassword = async () => {
  changingPassword.value = true;

  try {
    if (!passwordForm.current_password) {
      alert("Current password is required");
      return;
    }

    if (!passwordForm.new_password) {
      alert("New password is required");
      return;
    }

    if (passwordForm.new_password.length < 8) {
      alert("Password must be at least 8 characters");
      return;
    }

    if (passwordForm.new_password !== passwordForm.confirm_password) {
      alert("Passwords do not match");
      return;
    }

    await changePassword(
      passwordForm.current_password,
      passwordForm.new_password,
      authStore.token
    );

    resetPasswordForm();
    alert("Password changed successfully!");
  } catch (error) {
    alert(
      `Password change failed: ${error.response?.data?.detail || error.message}`
    );
  } finally {
    changingPassword.value = false;
  }
};

const resetProfileForm = () => {
  Object.assign(profileForm, originalProfile.value);
};

const resetPasswordForm = () => {
  passwordForm.current_password = "";
  passwordForm.new_password = "";
  passwordForm.confirm_password = "";
};

onMounted(() => {
  loadUserData();
});
</script>
