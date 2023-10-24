import LoginLayout from "../layouts/LoginLayout.vue"
import AdminLayout from "../layouts/AdminLayout.vue"
const routes = [
  // {
  //   path: '/',
  //   component: () => import('layouts/MainLayout.vue'),
  //   children: [
      
  //     { path: '', component: () => import('pages/IndexPage.vue') }
      
  //   ]
  // },
  {
    path: '/login',
    name: 'LoginLayout',
    props: true,
    component: LoginLayout
  },
  {
    path: '/',
    name: 'AdminLayout',
    props: true,
    component: AdminLayout
  },
  // Always leave this as last one,
  // but you can also remove it
  // {
  //   path: '/:catchAll(.*)*',
  //   component: () => import('pages/ErrorNotFound.vue')
  // }
]

export default routes
