<template>
  <div class="centro-informacion">
    [---CENTROINFO COMPONENT----]
    <h5>{{ msg }}...</h5>
    <br>
    <a href="">ir a sacar un turno para el centro elegido</a>
    <br>
    <br>
    [---/ CENTROINFO COMPONENT----]
  </div>
</template>

<script>
export default {
  name: 'CentroInfo',
  props: ['msg']
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
