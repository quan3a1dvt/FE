import LoginLayout from "../layouts/LoginLayout.vue"
import SamplesLayout from "../layouts/SamplesLayout.vue"
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      
      { path: '', component: () => import('pages/IndexPage.vue') }
      
    ]
  },
  {
    path: '/login',
    name: 'LoginLayout',
    props: true,
    component: LoginLayout
  },
  {
    path: '/sample',
    name: 'SamplesLayout',
    props: true,
    component: SamplesLayout
  },
  // Always leave this as last one,
  // but you can also remove it
  // {
  //   path: '/:catchAll(.*)*',
  //   component: () => import('pages/ErrorNotFound.vue')
  // }
]

export default routes
