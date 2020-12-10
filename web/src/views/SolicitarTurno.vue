<template>
  <div>
    <h1 class="p-3">Formulario de turno...</h1>
    <b-form @submit="onSubmit">
      <b-form-group
        id="input-group-1"
        label="Nombre:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.name"
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
          v-model="form.lastName"
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
      <label for="example-datepicker">Choose a date</label>
      <b-form-datepicker id="example-datepicker" v-model="form.date" @input="get_appointments()" class="mb-2"></b-form-datepicker>
      <p>Date: '{{ form.date }}'</p>
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
              :options="[{ text: 'Choose...', value: null }, appointments]"
              :value="null"
            >
            </b-form-select>
          </div>
          <div v-else>
            <p> No hay turnos disponibles </p>
          </div>
        </div>
      </b-form-group>
      <b-button type="submit" variant="primary">Enviar datos</b-button>
    </b-form>
  </div>
</template>

<script>
const axios = require('axios').default
export default {
  data () {
    return {
      form: {
        name: '',
        lastName: '',
        email: '',
        date: ''
      },
      appointments: [],
      errors: [],
      showOn: false,
      loading: true,
      selected: null
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      alert(JSON.stringify(this.form))
    },
    get_appointments () {
      this.showOn = true
      axios.get('https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/centros/' + this.$route.params.id + '/turnos_disponibles?fecha=' + this.form.date)
        .then(response => {
          this.appointments = response.data.turnos
          console.log(this.appointments)
          this.loading = false
        })
        .catch(e => {
          this.errors.push(e)
          this.loading = false
        })
    }
  },
  computed: {
    appointment_each () {
      this.appointments.forEach(
        appointment => {
          appointment.start_time
        });
      return
    }
  }
}

</script>

<style scoped>

</style>
