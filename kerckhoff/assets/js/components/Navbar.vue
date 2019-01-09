<template>
  <b-navbar toggleable type="light" variant="light">
    <div class="container-fluid">
      <!-- <b-nav-toggle target="nav_collapse"></b-nav-toggle> -->

      <b-link class="navbar-brand" href="/">
        <div class="d-flex align-items-center branding">
          <img class="logo pr-1 mr-2" src="/static/img/db_logo.svg" />
          <span class="title font-weight-bold">
            KERCKHOFF
          </span>
        </div>
      </b-link>

      <b-collapse is-nav id="nav_collapse">

        <b-nav is-nav-bar>
          <b-nav-item>Pages</b-nav-item>
          <b-nav-item>Team</b-nav-item>
          <b-nav-item href='/accounts/profile'>Profile</b-nav-item>
        </b-nav>

        <b-nav is-nav-bar class="ml-auto">
          <b-nav-item>
            <icon name="search"></icon>
          </b-nav-item>
        </b-nav>
      </b-collapse>

    </div>
  </b-navbar>
</template>

<script>
export default {
  name: 'navbar'
}
</script>

<style lang="scss" scoped>
.branding {
  .logo {
    width: 200px;
    border-right: 1px solid #333;
  }

  .title {
    font-size: 0.8em;
  }
}
</style>

