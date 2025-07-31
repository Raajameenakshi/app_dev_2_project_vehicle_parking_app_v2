import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Auth/login.vue'
import Register from '@/views/Auth/register.vue'
// import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
    },
    {
  path: '/admin',
  name: 'AdminDashboard',
  component: () => import('@/views/admin/AdminDashboard.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/view-users',
  name: 'AdminUsers',
  component: () => import('@/views/admin/adminusers.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/manage-lots',
  name: 'AdminParkingLots',
  component: () => import('@/views/admin/managelots.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/parking-lots/create',
  name: 'AdminCreateLot',
  component: () => import('@/views/admin/createlot.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/parking-lots/:id/edit',
  name: 'AdminEditLot',
  component: () => import('@/views/admin/editlot.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/parking-lots/:id',
  name: 'AdminViewLot',
  component: () => import('@/views/admin/viewlot.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/spots/:id',
  name: 'AdminViewSpot',
  component: () => import('@/views/admin/viewspot.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/spots/:id/booking',
  name: 'AdminSpotBooking',
  component: () => import('@/views/admin/spotbooking.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/bookings',
  name: 'ParkingRecords',
  component: () => import('@/views/admin/parkingrecords.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/admin/summary',
  name: 'Summary',
  component: () => import('@/views/admin/summary.vue'),
  meta: { requiresAuth: true, role: 'admin' }
},
{
  path: '/user',
  name: 'UserDashboard',
  component: () => import('@/views/user/UserDashboard.vue'),
  meta: { requiresAuth: true, role: 'user' }
},
{
  path: '/reserve/:lotId',
  name: 'ReserveSpot',
  component: () => import('@/views/user/reservespot.vue'),
  meta: { requiresAuth: true, role: 'user' }
},{
  path: '/release/:bookingId',
  name: 'ReleaseSpot',
  component: () => import('@/views/user/releasespot.vue'),
  meta: { requiresAuth: true, role: 'user' }
},{
  path: '/summary',
  name: 'UserSummary',
  component: () => import('@/views/user/summary.vue'),
  meta: { requiresAuth: true, role: 'user' }
},


]
})

export default router
