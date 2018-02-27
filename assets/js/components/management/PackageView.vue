<template>
  <div class="container">
    <div class="row">
      <div class="col">
      <h2>
        {{ packageData.slug || $route.params.slug }}
        <b-button class="ml-2" size="sm" variant="secondary" :disabled="isFetching" @click="fetchGdrive">
          <span v-if="isFetching">
            Fetching...
          </span>
          <span v-else>
            Update from GDrive
          </span>
        </b-button>
      </h2>
    </div>
    </div>
    <div class="col">
    <div class="row">
      <h5 class="text-muted">
        {{ packageData.description }}
      </h5>
    </div>
    </div>
    <div class="row">
      <div class="col-md-8">
        <h3 v-if="isLoading">
          Loading...
        </h3>
        <div v-else>
          <h5>Preview</h5>
          <div v-html="compiledMd"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {axios, utils} from "../../util";
import Vue from "vue";
import marked from "marked";

export default {
  name: 'package-view',
  computed: {
    compiledMd: function() {
      if(!this.packageData.cached_article_preview)
        return ""
      else {
        return marked(this.packageData.cached_article_preview, { sanitize: true })
      }
    }
  },
  data() {
    return {
      packageData: {},
      isFetching: false,
      isLoading: true,
    }
  },
  beforeMount: function() {
    axios.get("/api/packages/" + this.$route.params.slug + "/")
      .then((res) => {
        this.packageData = res.data;
        this.isLoading = false;
        console.log(this.packageData);
      })
  },
  methods: {
    fetchGdrive: function() {
      this.isFetching = true;
      axios.post("/api/packages/" + this.$route.params.slug + "/fetch")
        .then((res) => {
          console.log("Done fetching........")
          this.isFetching = false;
          console.log(res.data);
          this.packageData = res.data;
        })
    }
  }
}
</script>
