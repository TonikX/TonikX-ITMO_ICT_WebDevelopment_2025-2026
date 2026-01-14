<template>
  <div class="container">
    <div class="card" style="max-width:480px; margin:24px auto;">
      <h2 class="h1">Sign in</h2>
      <p class="small">Use your username and password to get JWT token (POST /api/token/)</p>

      <div class="form-row">
        <div class="form-control">
          <label>Username</label>
          <input class="input" v-model="form.username" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-control">
          <label>Password</label>
          <input type="password" class="input" v-model="form.password" />
        </div>
      </div>

      <div style="display:flex; gap:8px; justify-content:flex-end; margin-top:12px;">
        <button class="btn secondary" @click="reset">Reset</button>
        <button class="btn" @click="submit" :disabled="loading">
          <span v-if="loading">Signing…</span>
          <span v-else>Sign in</span>
        </button>
      </div>

      <p v-if="error" class="small" style="color:var(--danger); margin-top:12px;">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import auth from "@/services/auth";
import api from "@/services/api";
export default {
  data() {
    return {
      form: { username: "", password: "" },
      loading: false,
      error: null,
    };
  },
  methods: {
    reset() {
      this.form.username = "";
      this.form.password = "";
      this.error = null;
    },
    async submit() {
      this.error = null;
      this.loading = true;
      try {
        await auth.login(this.form.username, this.form.password);
        // optional: fetch current user info if endpoint exists
        // redirect back to home or previous
        this.$router.push({ name: "Home" });
      } catch (e) {
        console.error(e);
        this.error = (e.response && e.response.data && JSON.stringify(e.response.data)) || "Login failed";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>