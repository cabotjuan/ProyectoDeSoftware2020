<template>
  <div>
    <h1 class="p-3 mb-4 bg-info text-white text-center"><b-icon-graph-up></b-icon-graph-up> Estadísticas</h1>
    <b-container fluid class="section-servicio2">
          <b-row class="justify-content-center">
          <b-col md="6" class="justify-items-center">
            <h2 class="text-center m-4">Rótulo Gráfico 1</h2>
            <ve-pie :data="chartData" :settings="chartSettings" :id="Grafico1"></ve-pie>
            <hr>
          </b-col>
          <b-col md="6" class="justify-items-center">
            <h2 class="text-center m-4">Rótulo Gráfico 2</h2>
            <ve-pie :data="chartData" :settings="chartSettings" :id="Grafico1"></ve-pie>
            <hr>
          </b-col>
          </b-row>
          <b-row>
          <b-col md="6" class="justify-items-center">
            <h2 class="text-center m-4">Rótulo Gráfico 3</h2>
            <ve-pie :data="chartData" :settings="chartSettings" :id="Grafico1"></ve-pie>
          </b-col>
          <b-col md="6" class="justify-items-center">
            <h2 class="text-center m-4">Rótulo Gráfico 4</h2>
            <ve-pie :data="chartData" :settings="chartSettings" :id="Grafico1"></ve-pie>
          </b-col>
          </b-row>
    </b-container>
  </div>
</template>
<script>
import VePie from 'v-charts/lib/pie.common'
export default {
  components: { VePie },
  data () {
    this.chartSettings = {
      dimension: 'cost',
      metrics: 'profit'
    }
    return {
      chartData: {
        columns: ['date', 'cost', 'profit'],
        rows: [
          { date: '01/01', cost: 123, profit: 3 },
          { date: '01/02', cost: 1223, profit: 6 },
          { date: '01/03', cost: 2123, profit: 90 },
          { date: '01/04', cost: 4123, profit: 12 },
          { date: '01/05', cost: 3123, profit: 15 },
          { date: '01/06', cost: 7123, profit: 20 }
        ]
      }
    }
  }
}

/*
Gráfico 1. Cantidad de turnos atendidos por centro. Torta.
Gráfico 2. Gráfico por centro en un año, cantidad de turnos atendidos por mes. Gráfico en barras.
Gráfico 3. Cantidad de centros por municipio. Torta.
Gráfico 4(juan). Tipos de centros en base a total. Torta supongo.
*/

</script>
