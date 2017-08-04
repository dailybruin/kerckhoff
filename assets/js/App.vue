<template>
  <div class="main">
    <Navbar />
    <div class="container mt-5">
      <b-jumbotron header="BootstrapVue" lead="Bootstrap 4 Components for Vue.js 2">
        <p>For more information visit website</p>
        <b-btn variant="primary" href="#">Docs</b-btn>
      </b-jumbotron>
    </div>
    <PageFoot />
  </div>
</template>

<script>
import Navbar from './components/Navbar'
import PageFoot from './components/Footer'

export default {
  components: {
    Navbar,
    PageFoot
  },
  name: 'app'
}
</script>
