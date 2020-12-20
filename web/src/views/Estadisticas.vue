<template>
  <div>
    <h1 class="p-3 mb-4 bg-info text-white text-center"><b-icon-graph-up></b-icon-graph-up> Estadísticas</h1>
    <b-container fluid class="section-servicio2">
          <b-row class="justify-content-center">
          <b-col md="6" class="justify-items-center">
            <h2 class="text-center m-4">Centros por municipio</h2>
            <ve-pie :data="chartData1" :settings="chartSettings1"></ve-pie>
          </b-col>
          <b-col md="6" class="justify-items-center">
            <h2 class="text-center m-4">Turnos por Centro</h2>
            <ve-pie :data="chartDataTurnos" :settings="chartSettingsTurnos"></ve-pie>
          </b-col>
          <b-col md="6" class="justify-items-center">
            <h2 class="text-center m-4">Tipos de Centros</h2>
            <ve-histogram :data="chartDataCenterType"></ve-histogram>
          </b-col>
          </b-row>
    </b-container>
  </div>
</template>
<script>
import VePie from 'v-charts/lib/pie.common'
import VeHistogram from 'v-charts/lib/histogram.common'
const axios = require('axios').default
export default {
  components: { VePie, VeHistogram },
  data () {
    this.chartSettingsTurnos = {
      dimension: 'center',
      metrics: 'count'
    }
    this.chartSettings1 = {
      dimension: 'town',
      metrics: 'countCenter'
    }

    this.chartSettings = {
      dimension: 'cost',
      metrics: 'profit'
    }

    return {
      chartDataTurnos: {
        columns: ['center', 'count'],
        rows: []
      },
      chartData1: {
        columns: ['town', 'countCenter'],
        rows: []
      },
      chartDataCenterType: {
        columns: ['Tipos de centros', 'Merendero', 'Sociedad de Fomento', 'Iglesia', 'Sala', 'Otros'],
        rows: []
      }
    }
  },
  mounted () {
    axios.get('https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/centros')
      .then(response => {
        response.data.forEach(
          center => {
            const index = this.chartData1.rows.findIndex(row => row.town === center.town)
            if (index !== -1) {
              this.chartData1.rows[index].countCenter++
            } else {
              this.chartData1.rows.push({ town: center.town, countCenter: 1 })
            }
          })
      })
      .catch(e => {
        console.log(e)
      })
    axios.get('https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/centros/historial')
      .then(response => {
        response.data.forEach(
          row => {
            this.chartDataTurnos.rows.push({ center: row.center, count: row.appointments_count })
          }
        )
      })
    axios.get('https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/centros/tipos_de_centros')
      .then(response => {
        this.chartDataCenterType.rows.push(response.data)
      })
  }
}

</script>
