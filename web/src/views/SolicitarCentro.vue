<template>
  <div>
    <h1 class="p-3 mb-4 bg-info text-white text-center"><b-icon-plus></b-icon-plus> Solicitar Centro de Ayuda</h1>
    <b-container>
      <div v-if="ok">
        {{ get_towns() }}
      </div>
      <b-row class="justify-content-center">
        <b-col cols= "8">
          <b-form @submit.stop.prevent="post_center">
            <b-form-group
              id="input-group-1"
              label="Nombre:"
              label-for="input-1"
            >
              <b-form-input
                id="input-1"
                v-model="$v.form.name_center.$model"
                placeholder="Nombre"
                :state="validateState('name_center')"
              >
              </b-form-input>
            <div class="error text-danger" v-if="submited && !$v.form.name_center.required">Campo obligatorio.</div>
            </b-form-group>
            <b-form-group
              id="input-group-2"
              label="Dirección:"
              label-for="input-2"
            >
              <b-form-input
                id="input-2"
                v-model="$v.form.address.$model"
                :state="validateState('address')"
                placeholder="Dirección"
              ></b-form-input>
            <div class="error text-danger" v-if="submited && !$v.form.address.required">Campo obligatorio.</div>
            </b-form-group>
            <b-form-group
              id="input-group-3"
              label="Teléfono:"
              label-for="input-3"
            >
              <b-form-input
                id="input-3"
                v-model="$v.form.phone.$model"
                placeholder="Teléfono"
                :state="validateState('phone')"
              >
              </b-form-input>
              <div class="error text-danger" v-if="submited && !$v.form.phone.required">Campo obligatorio.</div>
              <div class="error text-danger" v-if="submited && !$v.form.phone.numeric">Solo numeros.</div>
            </b-form-group>
            <b-row>
              <b-col>
                <b-form-group
                  id="input-group-4"
                  label="Apertura:"
                  label-for="input-4"
                >
                <b-form-timepicker
                  v-model="$v.opening_time_sec.$model"
                  placeholder="Apertura"
                  locale="en"
                  :state="validateOpenState()"
                >
                </b-form-timepicker>
                <div class="error text-danger" v-if="submited && !$v.opening_time_sec.required">Campo obligatorio.</div>
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
                  v-model="$v.close_time_sec.$model"
                  placeholder="Cierre"
                  locale="en"
                  :state="validateCloseState()"
                >
                </b-form-timepicker>
                <div class="error text-danger" v-if="submited && !$v.close_time_sec.required">Campo obligatorio.</div>
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
                  v-model="$v.form.town.$model"
                  :options="sorted_array"
                  :state="validateState('town')"
                >
                </b-form-select>
                <div class="error text-danger" v-if="submited && !$v.form.town.required">Campo obligatorio.</div>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group
                  id="input-group-11"
                  label="Tipo de centro:"
                  label-for="input-11"
                >
                <b-form-select
                  v-model="$v.form.center_type_id.$model"
                  :options="center_types"
                  :state="validateState('center_type_id')"
                >
                </b-form-select>
                <div class="error text-danger" v-if="submited && !$v.form.center_type_id.required">Campo obligatorio.</div>
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
              v-model="$v.form.email.$model"
              placeholder="Email"
              :state="validateState('email')"
            >
            </b-form-input>
            <div class="error text-danger" v-if="submited && !$v.form.email.email">Email invalido.</div>
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
              <l-marker v-if="marker" :lat-lng="marker">
                <l-tooltip>{{ form.latitude }} - {{ form.longitude }}</l-tooltip>
              </l-marker>
              <l-tile-layer :url="url"></l-tile-layer>
            </l-map>
            </div>
            </b-form-group>
            <b-form-group
              id="input-group-verificar"
              label="Verificacion:"
              label-for="input-verificar"
            >
            <vue-recaptcha ref="recaptcha" @verify="onVerify" sitekey="6LezGQUaAAAAABBRwpY3FGileNcOiKk5RyM5-h4g"></vue-recaptcha>
            <div id="robot-msg" class="error text-danger" v-if="submited && !robot">Campo obligatorio.</div>
            </b-form-group>
            <b-button class= "mt-3" type="submit" variant="primary">Enviar datos</b-button>
            <b-button class= "mt-3 ml-2" type="cancel" variant="secondary" to="/">Cancelar</b-button>
          </b-form>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>
import { LMap, LTileLayer, LMarker, LTooltip } from 'vue2-leaflet'
import swal from 'sweetalert'
import VueRecaptcha from 'vue-recaptcha'
import { validationMixin } from 'vuelidate'
import { required, email, numeric } from 'vuelidate/lib/validators'
const axios = require('axios').default
export default {
  name: 'MyAwesomeMap',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    VueRecaptcha,
    LTooltip
  },
  mixins: [validationMixin],
  data () {
    return {
      form: {
        name_center: '',
        address: '',
        phone: '',
        opening_time: '',
        close_time: '',
        town: null,
        web: '-',
        email: '-',
        center_type_id: null,
        latitude: 0,
        longitude: 0,
        robot: false
      },
      submited: false,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 14,
      center: [-34.921408, -57.954555],
      marker: null,
      towns: [],
      errors: [],
      rango: [],
      ok: true,
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
  validations: {
    form: {
      name_center: {
        required
      },
      address: {
        required
      },
      town: {
        required
      },
      center_type_id: {
        required
      },
      email: {
        email
      },
      phone: {
        required,
        numeric
      }
    },
    opening_time_sec: {
      required
    },
    close_time_sec: {
      required
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
      this.submited = true
      this.$v.$touch()
      if (this.form.robot) {
        const msg = document.getElementById('robot-msg')
        if (msg) {
          msg.parentNode.removeChild(msg)
        }
      }
      if (this.$v.$invalid || !this.form.robot) {
        console.log('Error')
      } else {
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
      }
    },
    add_marker (event) {
      this.marker = event.latlng
      this.form.latitude = this.marker.lat
      this.form.longitude = this.marker.lng
    },
    set_opening_time () {
      this.form.opening_time = this.opening_time_sec.substring(0, 5)
    },
    set_close_time () {
      this.form.close_time = this.close_time_sec.substring(0, 5)
    },
    onVerify: function (response) {
      if (response) this.form.robot = true
    },
    validateState (n) {
      console.log(n)
      const { $dirty, $error } = this.$v.form[n]
      return $dirty ? !$error : null
    },
    validateOpenState () {
      const { $dirty, $error } = this.$v.opening_time_sec
      return $dirty ? !$error : null
    },
    validateCloseState () {
      const { $dirty, $error } = this.$v.close_time_sec
      return $dirty ? !$error : null
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
