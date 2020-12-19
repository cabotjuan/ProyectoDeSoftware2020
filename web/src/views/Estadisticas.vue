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
            <ve-pie :data="chartDataCenterType" :settings="chartSettingsCenterType"></ve-pie>
          </b-col>
          </b-row>
    </b-container>
  </div>
</template>
<script>
import VePie from 'v-charts/lib/pie.common'
const axios = require('axios').default
export default {
  components: { VePie },
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

    this.chartSettingsCenterType = {
      dimension: 'centerType',
      metrics: 'countCenterType'
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
        columns: ['centerType', 'countCenterType'],
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
        response.data.forEach(
          res => {
            this.chartDataCenterType.rows.push({ centerType: res.center_type, countCenterType: res.centers_count })
          }
        )
      })
  }
}

</script>
