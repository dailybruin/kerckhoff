<template>
  <b-navbar toggleable type="light" variant="light">
    <div class="container-fluid">
      <!-- <b-nav-toggle target="nav_collapse"></b-nav-toggle> -->

      <b-link class="navbar-brand" href="/">
        <div class="d-flex align-items-center branding">
          <img class="logo pr-1 mr-2" src="/static/img/db_logo.svg">
          <span class="title font-weight-bold">KERCKHOFF</span>
        </div>
      </b-link>

      <b-collapse is-nav id="nav_collapse">
        <b-nav is-nav-bar>
          <b-nav-item href="/manage">Manage</b-nav-item>
        </b-nav>

        <!-- <b-nav is-nav-bar class="ml-auto" v-if="authenticated">
          <b-nav-item-dropdown v-bind:text="currentPackage || 'Select a Package Set'" right>
            <b-dropdown-item v-for="context in contexts">{{ context }}</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-nav>-->
      </b-collapse>
    </div>
  </b-navbar>
</template>

<script>
import { axios } from "../util";

export default {
  name: "navbar",
  data: function() {
    return {
      contexts: []
    };
  },
  computed: {
    currentPackage: function() {
      const contextRegex = /\/manage\/([\w-]+)/m;
      const matches = this.$route.path.match(contextRegex);
      if (matches != null) {
        if (this.contexts.includes(matches[1])) return matches[1];
      }
      return null;
    }
  },
  props: {
    authenticated: {
      type: Boolean,
      default: false
    }
  }
  // beforeMount: function() {
  //   axios.get("/api/v2/package-set").then(d => {
  //     this.contexts = d.data.map(i => i.slug);
  //   });
  // }
};
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

