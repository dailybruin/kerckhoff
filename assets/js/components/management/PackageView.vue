<template>
  <div class="container">
    <div class="row">
      <div class="col">
      <h2>
        {{ packageData.slug || $route.params.slug }}
        <b-button class="ml-2" size="sm" variant="secondary" :disabled="isReallyFetching || isPublishing" @click="fetchGdrive">
          <span v-if="isReallyFetching">
            Fetching...
          </span>
          <span v-else-if="isPublishing">
            Publishing...
          </span>
          <span v-else>
            Update from GDrive
          </span>
        </b-button>
        <b-button class="ml-2" size="sm" variant="danger" :disabled="isReallyFetching || isPublishing" @click="publishToNode">
          <span v-if="isReallyFetching">
            Fetching...
          </span>
          <span v-else-if="isPublishing">
            Publishing...
          </span>
          <span v-else>
            Publish
          </span>
        </b-button>
      </h2>
      </div>
    </div>
    <div class="col">
    <div class="row">
      <h5 class="text-muted">
        {{ packageData.description }} | <a :href="packageData ? packageData.drive_folder_url : '#'" :disabled="isLoading"><small>Link</small></a>
      </h5>
    </div>
    </div>
    <div class="row">
      <div class="col-md-8">
        <h3 v-if="isLoading">
          Loading...
        </h3>
        <div v-else>
          <h5>Metadata</h5>
          <pre><code>{{fmMetaPretty}}</code></pre>

          <h5>Preview</h5>
          <div class="preview" v-html="compiledMd"></div>
        </div>
      </div>
      <div class="col-md-4" v-if="!isLoading">
        <h5>Images</h5>
        <div v-for="(image, key) in packageData.images.s3">
          <b-card :img-src="image.url"
                  :img-alt="image.key"
                  img-top class="mb-3">
              <p class="card-text">
                  <samp class="small">{{ image.url }}</samp>
              </p>
          </b-card>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.preview img {
  max-width: 100%;
}

code {
  max-width: 100%;
}

</style>



<script>
import {axios, utils} from "../../util";
import Vue from "vue";
import marked from "marked";
import matter from "gray-matter";

export default {
  name: 'package-view',
  computed: {
    isReallyFetching: function() {
      return this.isFetching || this.packageData.processing;
    },
    fmMetaPretty: function() {
      if(!this.packageData.cached_article_preview)
        return {}
      else {
        return JSON.stringify(matter(this.packageData.cached_article_preview).data, null, 2)
      }
    },
    compiledMd: function() {
      if(!this.packageData.cached_article_preview)
        return "Package is not fetched."
      else {
        return marked(matter(this.packageData.cached_article_preview).content, { sanitize: true })
      }
    }
  },
  data() {
    return {
      packageData: {},
      isFetching: false,
      isPublishing: false,
      isLoading: true,
    }
  },
  beforeMount: function() {
    axios.get("/api/packages/" + this.$route.params.pset + "/" + this.$route.params.slug + "/")
      .then((res) => {
        this.packageData = res.data;
        this.isLoading = false;
        console.log(this.packageData);
      })
  },
  methods: {
    fetchGdrive: function() {
      this.isFetching = true;
      axios.post("/api/packages/" + this.$route.params.pset + "/" + this.$route.params.slug + "/fetch")
        .then((res) => {
          console.log("Done fetching........")
          this.isFetching = false;
          console.log(res.data);
          this.packageData = res.data;
        })
    },
    publishToNode: function() {
      this.isPublishing = true;
      axios.post("/api/packages/" + this.$route.params.pset + "/" + this.$route.params.slug + "/push")
        .catch((error) => {
          alert("Publishing Failed!");
        });
      this.isPublishing = false;
    },
  }
}
</script>
