import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Centros from '../views/Centros.vue'
import Estadisticas from '../views/Estadisticas.vue'
import SolicitarCentro from '../views/SolicitarCentro.vue'
import SolicitarTurno from '../views/SolicitarTurno.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/centros',
    name: 'Centros',
    component: Centros
  },
  {
    path: '/centros/:id/solicitar_turno',
    name: 'Solicitar Turno',
    component: SolicitarTurno
  },
  {
    path: '/solicitar_centro',
    name: 'Solicitar Centro',
    component: SolicitarCentro
  },
  {
    path: '/estadisticas',
    name: 'Estadisticas',
    component: Estadisticas
  }
]

const router = new VueRouter({
  routes
})

export default router
