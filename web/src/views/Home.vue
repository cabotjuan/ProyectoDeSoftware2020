<template>
  <div class="home">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#2f9bae" fill-opacity="1" d="M0,192L1440,64L1440,0L0,0Z"></path></svg>
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
        </b-col>
        </b-row>
    </b-container>
    <div>
    </div>
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
</style>
