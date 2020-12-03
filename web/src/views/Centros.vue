<template>
  <div>
    [---CENTROS COMPONENT----]
    <h1>mapa de centros</h1>
    <CentroInfo :msg='msg'/>
    <br>
    [---/ CENTROS COMPONENT----]
  </div>
</template>
<script>

import CentroInfo from '@/components/CentroInfo.vue'

export default {
  name: 'Centros',
  components: {
    'CentroInfo':CentroInfo
    },
  data () {
    return {
      msg: 'Info de algun Centro de Ayuda elegido'
    }
  }

}

</script>
