<template>
  <aside :class="['sidebar', { closed: isClosed }]">
    <ul>
      <li>
        <span class="link-text" :class="[{ hidden: isClosed }, 'link-text-contrast']">Меню</span>
      </li>
      <li>
        <RouterLink to="/" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <Home class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Главная</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/employees" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <Users class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Сотрудники</span>
        </RouterLink>
      </li>
      <li>
        <span class="link-text" :class="[{ hidden: isClosed }, 'link-text-contrast']">Курицы</span>
      </li>
      <li>
        <RouterLink to="/chickens" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <Feather class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Курицы</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/breeds" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <Layers class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Породы</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/diets" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <Clipboard class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Диеты</span>
        </RouterLink>
      </li>
      <li>
        <span class="link-text" :class="[{ hidden: isClosed }, 'link-text-contrast']">Производство</span>
      </li>
      <li>
        <RouterLink to="/workshops" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <Factory class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Цехи</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/rows" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <Columns class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Ряды</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/cages" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <Birdhouse class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Клетки</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/egg-production" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <Egg class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Производство яиц</span>
        </RouterLink>
      </li>
      <li>
        <span class="link-text" :class="[{ hidden: isClosed }, 'link-text-contrast']">Отчеты</span>
      </li>
      <li>
        <RouterLink to="/report-factory-monthly" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <ClipboardList class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Ежемесячный отчет</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/report-breed-egg-difference" class="nav-link" active-class="active">
          <span class="icon-wrapper">
            <ClipboardList class="icon"/>
          </span>
          <span class="link-text" :class="{ hidden: isClosed }">Яйценоскость</span>
        </RouterLink>
      </li>
    </ul>
  </aside>
</template>


<script setup>
import {Home, Users, Feather, Layers, Clipboard, Factory, Columns, Box, ClipboardList, Birdhouse, Egg} from 'lucide-vue-next';

defineProps({
  isClosed: Boolean,
});

</script>

<style scoped>
.sidebar {
  width: 250px;
  background: var(--section-bg);
  font-weight: 500;
  font-size: 14px;
  transition: width 0.3s ease;
  flex-shrink: 0;
  overflow: hidden;
  padding-top: 20px;

  border-right: var(--border);
}

.sidebar.closed {
  width: 60px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar ul li {
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.link-text {
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
  max-width: 200px;
  opacity: 1;
  margin-left: 8px;
  transition: max-width 0.3s ease, opacity 0.3s ease, margin-left 0.3s ease;
  padding-left: 10px;
  color: var(--sidebar-text);
}

.link-text-contrast {
  font-weight: 600;
  padding-left: 0;
  margin: 0;
  color: var(--color);
}

.link-text.hidden {
  max-width: 0;
  opacity: 0;
  margin-left: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  color: inherit;
  text-decoration: none;
  width: 100%;
}

.icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  color: var(--sidebar-text);
  transition: color 0.3s ease;
}

.icon-wrapper {
  width: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
}
</style>
