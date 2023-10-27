<template>
  <footer class="footer">
    <div class="container">
      <div class="row justify-content-md-center">
        <div class="col col-md-auto">
          <span class="text-muted">&copy; 2017 The Daily Bruin</span>
        </div>
      </div>
      <div class="row justify-content-md-center mb-2">
        <div class="col col-md-auto">
          <span class="text-muted">Handcrafted with love in 118 Kerckhoff Hall</span>
        </div>
      </div>
      <div class="row justify-content-md-center text-center">
        <div class="col">
          <a href="#">About</a>
        </div>
        <div class="col">
          <a href="#">People</a>
        </div>
        <div class="col">
          <a href="#">Recruiting</a>
        </div>
        <div class="col">
          <a href="#">DailyBruin.com</a>
        </div>
        <div class="col">
          <a href="#">Bruinwalk</a>
        </div>
        <div class="col">
          <a href="/manage">Manage</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'page-foot'
}
</script>

<style lang="scss">

body {
  min-height: 100vh;
  position: relative;
  padding-bottom: 100px;
}

.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100px;
}

</style>

