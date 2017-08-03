<template>
  <div class="main">
    <Navbar />
    <div class="container mt-5">
      <b-jumbotron header="BootstrapVue" lead="Bootstrap 4 Components for Vue.js 2" >
        <p>For more information visit website</p>
        <b-btn variant="primary" href="#">Docs</b-btn>
      </b-jumbotron>
    </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar'

export default {
  components: {
    Navbar
  },
  name: 'app'
}
</script>
