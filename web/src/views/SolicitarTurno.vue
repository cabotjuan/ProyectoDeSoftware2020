<template>
  <div>
    <h1 class="p-3 mb-4 bg-info text-white text-center"><b-icon-calendar-date></b-icon-calendar-date> Solicitar turno</h1>
    <b-container>
      <b-row class="justify-content-center">
        <b-col cols= "8">
          <b-form @submit.stop.prevent="post_appointment">
            <b-form-group
              id="input-group-1"
              label="Nombre:"
              label-for="input-1"
              invalid-feedback="Campo obligatorio."
            >
              <b-form-input
                id="input-1"
                placeholder="Nombre"
                v-model="$v.form.first_name.$model"
                :state="validateState('first_name')"
              >
            </b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-2"
              label="Apellido:"
              label-for="input-2"
              invalid-feedback="Campo obligatorio."
            >
              <b-form-input
                id="input-2"
                placeholder="Apellido"
                v-model="$v.form.last_name.$model"
                :state="validateState('last_name')"
              ></b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-3"
              label="Dirección de correo electrónico:"
              label-for="input-3"
            >
              <b-form-input
                id="input-3"
                placeholder="Email"
                v-model="$v.form.email.$model"
                :state="validateState('email')"
              >
              </b-form-input>
            </b-form-group>
            <div class="error text-danger" v-if="submited && !$v.form.email.required">Campo obligatorio.</div>
            <div class="error text-danger" v-if="submited && !$v.form.email.email">E-mail no valido.</div>
            <b-form-group
              id="input-group-3"
              label="Teléfono:"
              label-for="input-3"
            >
              <b-form-input
                id="input-3"
                type="number"
                placeholder="Teléfono"
                v-model="$v.form.phone.$model"
                :state="validateState('phone')"
              >
              </b-form-input>
            </b-form-group>
            <div class="error text-danger" v-if="submited && !$v.form.phone.required">Campo obligatorio.</div>
            <div class="error text-danger" v-if="submited && !$v.form.phone.numeric">Solo numeros.</div>
            <label for="example-datepicker">Elegí una fecha</label>
            <b-form-datepicker id="example-datepicker" v-model="$v.form.appointment_date.$model" :state="validateState('appointment_date')" @input="get_appointments()" class="mb-2"></b-form-datepicker>
            <div class="error text-danger" v-if="submited && !$v.form.appointment_date.required">Campo obligatorio.</div>
            <b-form-group v-if="showOn" id="input-group-4" label="Horarios disponibles" label-for="input-4" >
              <div v-if="loading">
                <b-spinner variant="primary" label="Spinning"></b-spinner>
              </div>
              <div v-else>
                <div v-if="appointments.length">
                  <b-form-select
                    id="input-4"
                    class="mb-2 mr-sm-2 mb-sm-0"
                    v-model="$v.selected.$model"
                    :state="validateSelectedState()"
                    :options="appointment_each"
                    :value="null"
                  >
                  </b-form-select>
                </div>
                <div v-else>
                  <p> No hay turnos disponibles </p>
                </div>
              </div>
            <div class="error text-danger" v-if="submited && !$v.selected.required">Campo obligatorio.</div>
            </b-form-group>
            <b-button class= "mt-3" type="submit" variant="primary">Enviar datos</b-button>
            <b-button class= "mt-3 ml-2" type="cancel" variant="secondary" to="/centros">Cancelar</b-button>
          </b-form>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import swal from 'sweetalert'
import { validationMixin } from 'vuelidate'
import { required, email, numeric } from 'vuelidate/lib/validators'
const axios = require('axios').default
export default {
  mixins: [validationMixin],
  data () {
    return {
      form: {
        first_name: null,
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
      loading: true,
      submited: false
    }
  },
  validations: {
    form: {
      first_name: {
        required
      },
      last_name: {
        required
      },
      email: {
        required,
        email
      },
      appointment_date: {
        required
      },
      phone: {
        required,
        numeric
      }
    },
    selected: {
      required
    }
  },
  methods: {
    get_appointments () {
      this.showOn = true
      axios.get('https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/centros/' + this.$route.params.id + '/turnos_disponibles?fecha=' + this.form.appointment_date)
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
      this.submited = true
      this.$v.form.$touch()
      if (this.$v.form.$invalid) {
        console.log('error')
        return
      }
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
    },
    validateState (name) {
      const { $dirty, $error } = this.$v.form[name]
      return $dirty ? !$error : null
    },
    validateSelectedState () {
      const { $dirty, $error } = this.$v.selected
      return $dirty ? !$error : null
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
