<template>
  <div class="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {

}
</script>

<style>
.app {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 10;
    background: linear-gradient(135deg, #7a66ea 10%, #b84a65 100%);
}

.page {
  display: flex;
  gap: 20px;
}

.page-title {
  margin-top: 0;
  margin-bottom: 30px;
  font-size: 2rem;
  font-weight: 600;
  color: #2d3748;
  text-align: center;
  letter-spacing: -0.5px;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 15px;
}

.page > :last-child {
  flex: 1;
  min-width: 0;
}

.filter-section {
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(247, 250, 252, 0.8);
  border-radius: 16px;
  border: 1px solid rgba(226, 232, 240, 0.6);
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 12px;
}

.filter-input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
  transition: all 0.2s;
}

.filter-input:focus {
  outline: none;
  border-color: #7a66ea;
  box-shadow: 0 0 0 3px rgba(122, 102, 234, 0.1);
}

.filter-row {
  display: flex;
  flex-wrap: nowrap;
  align-items: flex-end;
}

.filter-item {
  min-width: 160px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-item.button-item {
  flex: 0 0 auto;
  margin-left: auto;
}

.filter-item label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #4a5568;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  white-space: nowrap;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #2d3748;
}

.empty-message {
  text-align: center;
  font-size: 1.2rem;
  color: #4a5568;
  background: #edf2f7;
  padding: 30px;
  border-radius: 12px;
  margin: 20px 0 0;
}
</style>
