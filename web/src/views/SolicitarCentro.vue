<template>
  <div>
    <h1 class="p-3 mb-4 bg-info text-white text-center">¿Desea cargar un Centro de Ayuda?</h1>
    <b-container>
      <div v-if="ok">
        {{ get_towns() }}
      </div>
      <b-row class="justify-content-center">
        <b-col cols= "8">
          <b-form @submit="post_center">
            <b-form-group
              id="input-group-1"
              label="Nombre:"
              label-for="input-1"
            >
              <b-form-input
                id="input-1"
                v-model="form.name_center"
                required
                placeholder="Nombre"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-2"
              label="Dirección:"
              label-for="input-2"
            >
              <b-form-input
                id="input-2"
                v-model="form.address"
                required
                placeholder="Dirección"
              ></b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-3"
              label="Teléfono:"
              label-for="input-3"
            >
              <b-form-input
                id="input-3"
                v-model="form.phone"
                type="number"
                required
                placeholder="Teléfono"
              >
              </b-form-input>
            </b-form-group>
            <b-row>
              <b-col>
                <b-form-group
                  id="input-group-4"
                  label="Apertura:"
                  label-for="input-4"
                >
                <b-form-timepicker
                  v-model="opening_time_sec"
                  placeholder="Apertura"
                  locale="en"
                >
                </b-form-timepicker>
                <div v-if="opening_time_sec">
                  {{ set_opening_time() }}
                </div>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group
                  id="input-group-5"
                  label="Cierre:"
                  label-for="input-5"
                >
                <b-form-timepicker
                  v-model="close_time_sec"
                  placeholder="Cierre"
                  locale="en"
                >
                </b-form-timepicker>
                <div v-if="close_time_sec">
                  {{ set_close_time() }}
                </div>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row>
              <b-col cols=6>
                <b-form-group
                  id="input-group-6"
                  label="Municipios:"
                  label-for="input-6"
                >
                <b-form-select
                  v-model="form.town"
                  :options="sorted_array"
                >
                </b-form-select>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group
                  id="input-group-11"
                  label="Tipo de centro:"
                  label-for="input-11"
                >
                <b-form-select
                  v-model="form.center_type_id"
                  :options="center_types"
                >
                </b-form-select>
                </b-form-group>
              </b-col>
            </b-row>
            <b-form-group
              id="input-group-7"
              label="Página web:"
              label-for="input-7"
            >
            <b-form-input
              id="input-7"
              v-model="form.web"
              required
              placeholder="Página web"
            >
            </b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-8"
              label="Email:"
              label-for="input-8"
            >
            <b-form-input
              id="input-8"
              v-model="form.email"
              type="email"
              required
              placeholder="Email"
            >
            </b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-9"
              label="Protocolo de visita:"
              label-for="input-9"
            >
            <b-form-file
              id="input-9"
              v-model="visit_protocol_object"
              class="mt-3"
              plain
            >
            </b-form-file>
            <div v-if="visit_protocol_object">
              {{ set_visit_protocol() }}
            </div>
            </b-form-group>
            <b-form-group
              id="input-group-10"
              label="Ubicación:"
              label-for="input-10"
            >
            <div class="px-3" style="height: 500px">
            <l-map
              style="height: 90%; width: 100%; display: flex;"
              :zoom="zoom"
              :center="center"
              @click="add_marker"
              id='map'
            >
              <l-marker v-if="marker" :lat-lng="marker"></l-marker>
              <l-tile-layer :url="url"></l-tile-layer>
            </l-map>
            </div>
            </b-form-group>
            <b-button class= "mt-4" type="submit" variant="primary">Enviar datos</b-button>
          </b-form>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet'
import swal from 'sweetalert'
const axios = require('axios').default
export default {
  name: 'MyAwesomeMap',
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  data () {
    return {
      form: {
        name_center: '',
        address: '',
        phone: '',
        opening_time: '',
        close_time: '',
        town: null,
        web: '',
        email: '',
        visit_protocol: '',
        center_type_id: null,
        latitude: 0,
        longitude: 0
      },
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 14,
      center: [-34.921408, -57.954555],
      marker: null,
      towns: [],
      errors: [],
      rango: [],
      ok: true,
      visit_protocol_object: null,
      opening_time_sec: '',
      close_time_sec: '',
      center_types: [
        { value: null, text: 'Elegí una opción' },
        { value: 1, text: 'Merendero' },
        { value: 2, text: 'Sociedad de Fomento' },
        { value: 3, text: 'Iglesia' },
        { value: 4, text: 'Sala' },
        { value: 5, text: 'Otros' }
      ]
    }
  },
  methods: {
    get_towns () {
      axios.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios')
        .then(response => {
          this.ok = false
          const len = Math.ceil(response.data.total / response.data.per_page) + 1
          for (let x = 1; x < len; x++) {
            this.rango.push(x)
          }
          for (const page in this.rango) {
            axios.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=' + this.rango[page])
              .then(res => {
                for (const element in res.data.data.Town) {
                  this.towns.push(res.data.data.Town[element])
                }
              })
          }
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    post_center () {
      axios.post('https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/centros', this.form)
        .then(response => {
          swal('¡Listo!', 'El centro se cargó correctamente', 'success')
            .then(() => {
              this.$router.push({ name: 'Home' })
            })
        })
        .catch(e => {
          console.log(e)
        })
    },
    add_marker (event) {
      this.marker = event.latlng
      this.form.latitude = this.marker.lat
      this.form.longitude = this.marker.lng
      console.log(this.form)
    },
    set_visit_protocol () {
      this.form.visit_protocol = this.visit_protocol_object.name
    },
    set_opening_time () {
      this.form.opening_time = this.opening_time_sec.substring(0, 5)
    },
    set_close_time () {
      this.form.close_time = this.close_time_sec.substring(0, 5)
    }
  },
  computed: {
    town_each () {
      var arrTowns = [{ value: null, text: 'Elegí un municipio' }]
      this.towns.forEach(
        town => {
          arrTowns.push({ value: town.name, text: town.name })
        })
      return arrTowns
    },
    sorted_array: function () {
      function compare (a, b) {
        if (a.text < b.text) {
          return -1
        }
        if (a.text > b.text) {
          return 1
        }
        return 0
      }
      return this.town_each.slice().sort(compare)
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
