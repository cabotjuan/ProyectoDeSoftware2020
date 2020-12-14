<template>
  <div class="home">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#2f9bae" fill-opacity="1" d="M0,96L120,90.7C240,85,480,75,720,80C960,85,1200,107,1320,117.3L1440,128L1440,0L1320,0C1200,0,960,0,720,0C480,0,240,0,120,0L0,0Z"></path></svg>
    <b-container fluid class="section-descripcion">
      <b-row>
      <b-col md="6">
        <b-img :src="require('@/assets/marginalia-girl-came-to-visit-her-friend.png')" fluid-grow></b-img>
      </b-col>
      <b-col md="6">
        <h1 class="banner-title">Encontrá ayuda.</h1>
        <h5>Centros de Ayuda - Provincia de Buenos Aires</h5>
        <br>
        <p class="descripcion">Sabemos que el 2020 ha sido un año muy difícil para toda la región. <br> Por eso, desde <b> Centros de Ayuda GBA</b>, brindamos una posibilidad de ayuda a aquellos que más lo necesitan. También podrás dar una mano donando comida, ropa, plasma o sangre acercándote a cualquier Centro de Ayuda solicitando un turno previamente.
        </p>
        <br>
        <h6 class="font-weight-light">Encontrá el Centro de Ayuda más cercano acá:</h6><br>
        <b-button block pill variant="info" size="lg" class="w-50" to="/centros"><b-icon-map></b-icon-map> Ver Mapa</b-button>
        <br>
      </b-col>
      </b-row>
    </b-container>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#2f9bae" fill-opacity="1" d="M0,128L120,138.7C240,149,480,171,720,165.3C960,160,1200,128,1320,112L1440,96L1440,320L1320,320C1200,320,960,320,720,320C480,320,240,320,120,320L0,320Z"></path></svg>
    <b-container fluid class="section-servicio1">
          <b-row>
          <b-col md="6">
            <b-img style="max-width:240px;" :src="require('@/assets/Center3.png')" fluid></b-img>
          </b-col>
          <b-col md="6">
            <h2 class="banner-title">Solicitar nuevo Centro</h2>
            <br>
            <p class="descripcion2">Si disponés o conocés algún lugar que pueda brindar ayuda de cualquier tipo, solicitá incorporarlo al mapa así lo pueden encontrar.
            </p>
            <br>
            <b-button pill variant="success" size="lg" to="/solicitar_centro"><b-icon-plus></b-icon-plus>  Solicitar</b-button>
          </b-col>
          </b-row>
    </b-container>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#2f9bae" fill-opacity="1" d="M0,96L120,90.7C240,85,480,75,720,80C960,85,1200,107,1320,117.3L1440,128L1440,0L1320,0C1200,0,960,0,720,0C480,0,240,0,120,0L0,0Z"></path></svg>
    <b-container fluid class="section-servicio2">
          <b-row class="justify-content-center">
          <b-col md="4" class="p-4">
            <h2 class="banner-title">Estadísticas</h2>
            <br>
            <p class="descripcion"> Conocé los datos y estadísticas de la situación en toda la Provincia de Buenos Aires
            </p>
            <br>
            <b-button pill variant="primary" size="lg" to="/estadisticas"><b-icon-graph-up></b-icon-graph-up> Ver más </b-button>
          </b-col>
          <b-col md="6">
            <b-img :src="require('@/assets/clip-covid-19-spread-statistic.png')" fluid-grow></b-img>
          </b-col>
          </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style>
  .banner-title{
    font-weight: bolder;
  }
  .descripcion{
    text-align: start;
    line-height: 2rem;
    font-weight: normal;
    color: #7d7d7d;
  }
  .descripcion2{
    text-align: start;
    line-height: 2rem;
    font-weight: normal;
    color: #fafafa;
  }
  .section-servicio1{
    background-color: #2f9bae;
    color: #fafafa;
  }
  .section-servicio2{
    background-color: #fafafa;
  }
</style>
