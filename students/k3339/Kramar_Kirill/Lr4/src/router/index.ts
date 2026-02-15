import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RegisterView from '@/views/RegisterView.vue';
import LoginView from '@/views/LoginView.vue';
import TeacherListView from "@/views/TeacherListView.vue";
import ProfileView from "../views/ProfileView.vue";
import StudentListView from "../views/StudentListView.vue";
import ClassListView from "../views/ClassListView.vue";
import ClassroomListView from "../views/ClassroomListView.vue";
import ScheduleView from "../views/ScheduleView.vue";
import GradeListView from "../views/GradeListView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView
    },
    {
      path: '/profile',
      name: 'Profile',
      component: ProfileView
    },
    {
      path: '/teachers',
      name: 'Teachers',
      component: TeacherListView
    },
    {
      path: '/students',
      name: 'Students',
      component: StudentListView
    },
    {
      path: '/classes',
      name: 'Classes',
      component: ClassListView
    },
    {
      path: '/classrooms',
      name: 'Classrooms',
      component: ClassroomListView
    },
    {
      path: '/lessons',
      name: 'Schedule',
      component: ScheduleView
    },
    {
      path: '/grades',
      name: 'Grades',
      component: GradeListView
    },
  ],
})

export default router
