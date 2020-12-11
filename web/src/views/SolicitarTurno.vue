<template>
  <div>
    <h1 class="p-3 mb-4 bg-info text-white text-center">Solicitar turno</h1>
    <b-container>
      <b-row class="justify-content-center">
        <b-col cols= "8">
          <b-form @submit="post_appointment">
            <b-form-group
              id="input-group-1"
              label="Nombre:"
              label-for="input-1"
            >
              <b-form-input
                id="input-1"
                v-model="form.first_name"
                required
                placeholder="Nombre"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-2"
              label="Apellido:"
              label-for="input-2"
            >
              <b-form-input
                id="input-2"
                v-model="form.last_name"
                required
                placeholder="Apellido"
              ></b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-3"
              label="Dirección de correo electrónico:"
              label-for="input-3"
            >
              <b-form-input
                id="input-3"
                v-model="form.email"
                type="email"
                required
                placeholder="Email"
              >
              </b-form-input>
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
            <label for="example-datepicker">Elegí una fecha</label>
            <b-form-datepicker id="example-datepicker" v-model="form.appointment_date" @input="get_appointments()" class="mb-2"></b-form-datepicker>
            <b-form-group v-if="showOn" id="input-group-5" label="Horarios disponibles">
              <div v-if="loading">
                <b-spinner variant="primary" label="Spinning"></b-spinner>
              </div>
              <div v-else>
                <div v-if="appointments.length">
                  <b-form-select
                    id="inline-form-custom-select-pref"
                    class="mb-2 mr-sm-2 mb-sm-0"
                    v-model="selected"
                    :options="appointment_each"
                    :value="null"
                  >
                  </b-form-select>
                  {{ selected }}
                </div>
                <div v-else>
                  <p> No hay turnos disponibles </p>
                </div>
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
import swal from 'sweetalert'
const axios = require('axios').default
export default {
  data () {
    return {
      form: {
        first_name: '',
        last_name: '',
        email: '',
        appointment_date: '',
        start_time: null,
        end_time: null,
        center_id: this.$route.params.id,
        phone: null
      },
      selected: null,
      appointments: [],
      errors: [],
      showOn: false,
      loading: true
    }
  },
  methods: {
    get_appointments () {
      this.showOn = true
      const config = {
        headers: {
          'Acces-Control-Allow-Origin': '*'
        }
      }
      axios.get('https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/centros/' + this.$route.params.id + '/turnos_disponibles?fecha=' + this.form.appointment_date, config)
        .then(response => {
          this.appointments = response.data.appointments
          this.loading = false
        })
        .catch(e => {
          this.errors.push(e)
          this.loading = false
        })
    },
    post_appointment () {
      axios.post('https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/centros/' + this.$route.params.id + '/reserva', this.form)
        .then(response => {
          swal('¡Listo!', 'Tu turno ha sido reservado', 'success')
            .then(() => {
              this.$router.push({ name: 'Home' })
            })
        })
        .catch(e => {
          console.log(e)
        })
    }
  },
  computed: {
    appointment_each () {
      var arrApp = [{ value: null, text: 'Elegí un horario' }]
      this.appointments.forEach(
        appointment => {
          arrApp.push({ value: { start: appointment.start_time, end: appointment.end_time }, text: appointment.start_time + ' - ' + appointment.end_time })
        })
      return arrApp
    }
  },
  watch: {
    selected: function () {
      this.form.start_time = this.selected.start
      this.form.end_time = this.selected.end
    }
  }
}

</script>

<style scoped>

</style>
