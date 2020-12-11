<template>
  <div>
    <h1 class="p-3 mb-4 bg-info text-white text-center"><b-icon-map></b-icon-map> Centros de Ayuda</h1>
    <b-row>
      <b-col b-col>
        <div class="px-3" style="height: 500px">

          <l-map
            style="height: 90%; width: 100%; display: flex;"
            :zoom="zoom"
            :center="center"
            id='map'
          >
            <div v-if="centers && centers.length">
              <l-marker v-on:click="show_center(c)" v-for="c in centers" :key="c.id" :lat-lng="[c.latitude, c.longitude]">
                <l-popup>
                  {{ c.name_center }}
                </l-popup>
              </l-marker>
            </div>

            <l-tile-layer :url="url"></l-tile-layer>
          </l-map>
        </div>
      </b-col>
      <transition name="fade">
        <b-col v-if="showOn" b-col cols="4">
          <b-container class="pl-0" fluid style="height: 500px">
            <b-row class="justify-content-end mr-4">
              <h1>
                <b-link>
                  <b-icon-x-circle v-on:click="close_info()"></b-icon-x-circle>
                </b-link>
              </h1>
            </b-row>
            <b-row>
              <h2>{{ centerData.name_center }} </h2>
            </b-row>
            <br>
            <b-row>
              <h5>Dirección: {{ centerData.address }}</h5>
            </b-row>
            <b-row>
              <h5>Municipio: {{ centerData.town }}</h5>
            </b-row>
            <b-row v-if="centerData.email" >
              <h5>
                Email: {{ centerData.email }}
              </h5>
            </b-row>
            <b-row v-else>
              <h5>
                Email: No disponible
              </h5>
            </b-row>
            <b-row>
              <h5> Teléfono: {{ centerData.phone }}</h5>
            </b-row>
            <b-row>
            <h5>Abierto: {{ centerData.opening_time }} - {{ centerData.close_time }} </h5>
            </b-row>
            <br>
            <b-button :id="centerData.id" block pill variant="info" size="lg" :to="this.$route.path + '/' + centerData.id + '/solicitar_turno'"><b-icon-calendar-date></b-icon-calendar-date> Solicitar turno </b-button>
          </b-container>
        </b-col>
      </transition>
    </b-row>
    <router-view />
  </div>
</template>
<script>
// import CentroInfo from '@/components/CentroInfo.vue'
// import L from 'leaflet'
// import { latLng } from 'leaflet'
import { LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet'
const axios = require('axios').default

export default {
  name: 'MyAwesomeMap',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 14,
      center: [-34.921408, -57.954555],
      // aPopup: latLng(-34.921408, -57.954555)
      centers: [],
      errors: [],
      centerData: '',
      showOn: false

    }
  },
  created () {
    axios.get('https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/centros')
      .then(response => {
      // JSON responses are automatically parsed.
        console.log(response.data)
        this.centers = response.data
      })
      .catch(e => {
        this.errors.push(e)
      })
  },
  methods: {
    show_center: function (dataCenter) {
      this.showOn = true
      this.centerData = dataCenter
      this.center = [this.centerData.latitude, this.centerData.longitude]
    },
    close_info: function () {
      this.showOn = false
    }
  }
}

</script>

<style scoped>
  .fade-enter-active, .fade-leave-active {
  transition: opacity .5s
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0
  }
</style>
