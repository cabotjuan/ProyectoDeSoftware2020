<template>
  <div id="app">
    <header>
      <b-navbar toggleable="md" type="dark">
        <b-link to="/">
          <b-navbar-brand>
            <img
              src="./assets/Logo.png"
              class="gba-logo"
              alt="Centros de Ayuda GBA"
            />
          </b-navbar-brand>
        </b-link>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-link to="/centros" class="nav-route-link">
              <b-icon-map></b-icon-map> Ver Centros
            </b-link>
            <b-link to="/solicitar_centro" class="nav-route-link">
              <b-icon-plus></b-icon-plus> Añadir centro
            </b-link>
            <b-link to="/estadisticas" class="nav-route-link">
              <b-icon-graph-up></b-icon-graph-up> Estadisticas
            </b-link>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </header>
    <section class="main-route-content">
        <router-view />
    </section>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#2f9bae" fill-opacity="1" d="M0,160L120,154.7C240,149,480,139,720,149.3C960,160,1200,192,1320,208L1440,224L1440,320L1320,320C1200,320,960,320,720,320C480,320,240,320,120,320L0,320Z"></path></svg>
    <footer class="footer-content">
      <b-container class="footer-container">
        <b-row class="footer-info-container1">
          <b-col><img
              src="./assets/LogoVertical.png"
              class="logo-vertical"
              alt="Centros de Ayuda GBA"
            />
            </b-col>
          <b-col class="align-items-end">
            <h5 class="footer-info"> Enlaces</h5>
            <b-link to="/" class="nav-route-link mt-1">
              Inicio
            </b-link><br>
            <b-link to="/centros" class="nav-route-link mt-4">
              Ver Centros
            </b-link><br>
            <b-link to="/solicitar_centro" class="nav-route-link mt-4">
              Añadir centro
            </b-link><br>
            <b-link to="/estadisticas" class="nav-route-link mt-4 mb-4">
            Estadisticas
            </b-link><br><h5 class="footer-info"> Uso Interno </h5>
            <b-link href="https://admin-grupo5.proyecto2020.linti.unlp.edu.ar/administracion/" class="nav-route-link mt-1">
            Administracion
            </b-link><br>
            </b-col>
        </b-row>
        <b-row class="footer-info-container2">
          <h6 class="footer-info">
          <b-icon-code></b-icon-code> Grupo 5 Proyecto de Software• 2020 • Facultad de Informática • Universidad Nacional de la Plata • Illustration:<a href="https://icons8.com/">Icons8</a>
          </h6>
        </b-row>
      </b-container>
    </footer>
  </div>
</template>
<script>
export default {
  created () {
    document.title = 'Centros de Ayuda GBA'
  }
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;500;700&display=swap");

#app {
  background-color: #fafafa;
  font-family: "Josefin Sans", sans-serif;
}

/* HEADER STYLES */

.nav-route-link {
  color: #fafafa;
  margin-left: 1rem;
  margin-right: 1rem;
  border-bottom: 2px solid #2f9bae;
  text-align: end;
}
.nav-route-link:hover {
  border-bottom: 2px solid #0e889d;
  font-weight: bold;
  text-decoration: none;
  color: #fafafa;
}
.navbar {
  background-color: #2f9bae;
}

/* ROUTER VIEW STYLES */

.main-route-content {
  min-height: 100vh;
  color: #555;
  background-color: #fafafa;
}

/* FOOTER STYLES */

.footer-content {
  height: 75vh;
  max-height: 350px;
  margin-top: -5px;
  background-color: #2f9bae;
}
.footer-container{
      display: flex;
    flex-direction: column;
    height: 100%;
}
.footer-info-container1{
  flex-direction: row;
  height: 100%;
  justify-content: end;
  align-content: baseline;
}

.logo-vertical{
  max-width: 220px;
}
.footer-info-container1 .col{
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
  align-items: flex-start;
}
.footer-info-container2{
  flex-direction: column;
  justify-content: end;
  align-content: center;
  flex-wrap: nowrap;
}
.footer-info{
  color: #fafafa;
  position: relative;
  bottom: 0;
  text-align: center;
  font-weight: lighter;
}
.footer-info  a {
  color: #fafafa;
  font-style: italic;
  }

</style>
