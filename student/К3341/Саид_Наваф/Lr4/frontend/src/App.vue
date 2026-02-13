<template>
  <div id="app">
    <header class="app-header">
      <nav class="nav">
        <div class="brand">Car Registry</div>
        <div class="nav-links">
          <router-link to="/" exact-active-class="active">Home</router-link>
          <router-link to="/owners" exact-active-class="active">Owners</router-link>
          <router-link to="/cars" exact-active-class="active">Cars</router-link>
          <router-link to="/vehicle-models" exact-active-class="active">Models</router-link>
        </div>
        <div style="margin-left:auto">
          <template v-if="loggedIn">
            <button class="btn secondary" @click="goProfile">Profile</button>
            <button class="btn" @click="logout">Sign out</button>
          </template>
          <template v-else>
            <router-link to="/login"><button class="btn">Sign in</button></router-link>
          </template>
        </div>
      </nav>
    </header>

    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<script>
import auth from "@/services/auth";
export default {
  data() {
    return { loggedIn: auth.isAuthenticated() };
  },
  created() {
    // listen to storage changes (in case of multiple tabs)
    window.addEventListener("storage", this.onStorage);
  },
  beforeUnmount() {
    window.removeEventListener("storage", this.onStorage);
  },
  methods: {
    onStorage() {
      this.loggedIn = auth.isAuthenticated();
    },
    logout() {
      auth.logout();
      this.loggedIn = false;
      this.$router.push({ name: "Login" });
    },
    goProfile() {
      // optionally navigate to profile or owner detail
      this.$router.push({ name: "Owners" });
    },
  },
};
</script>