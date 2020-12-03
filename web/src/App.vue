<template>
  <div id="app">
    [---APP COMPONENT----]
    <div id="nav">
      <router-link to="/"> Home </router-link>
      <router-link to="/centros"> Ver Centros </router-link>
      <router-link to="/solicitar_centro"> Solicitar nuevo centro </router-link>
      <router-link to="/estadisticas"> Estadisticas </router-link>
    </div>
    <hr>
    <router-view/>
    <br>
    [---/ APP COMPONENT----]
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #fafafa;
  background-color: #000;
  border-style: 5px solid;
  padding: 0.5 rem;
  margin: 0.5rem;
}
#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
