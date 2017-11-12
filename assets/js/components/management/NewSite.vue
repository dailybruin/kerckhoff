<template>
  <div>
    <h2 class="mb-3">New Site</h2>
    <b-form @submit="onSubmit">
      <h5>Site Type</h5>
      <b-form-radio v-model="form.siteType" :options="siteTypeOptions"></b-form-radio>
      <b-form-group v-if="form.siteType != 'Series'">
        <b-form-input type="text" v-model="form.slug" required placeholder="Enter site slug" description="This will be the URL path for the site" :formatter="formatSlug" lazy-formatter></b-form-input>
        <p>
          <small>{{ 'features.dailybruin.com/' + form.slug }}</small>
        </p>
      </b-form-group>
      <b-form-group v-else id="exampleInputGroup3" label="Food:" label-for="exampleInput3">
        <b-form-select id="exampleInput3" :options="foods" required v-model="form.food"></b-form-select>
      </b-form-group>
      <b-form-group class="uploadInput">
        <file-upload ref="uploadComponent" v-model="form.files" name="files" :multiple="true" :directory="true" drop=".drop-area" @input="newFile">
          <div @dragenter="dragHover = true" @dragover="dragHover = true" @dragleave="dragHover = false" :class=" { 'drag-on': dragHover } " class="drop-area">
            Drag and drop files here
          </div>
        </file-upload>
        <div v-show="form.files" class="uploadedFiles">
          <ul class="list-group w-100">
            <div v-for="file in form.files" :key="file.id" class="list-group-item">
              <div class="d-flex w-100 justify-content-between">
                <span>{{ file.name }}</span>
                <span>{{ file.progress }}</span>
              </div>
            </div>
          </ul>
        </div>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="secondary">Reset</b-button>
    </b-form>
  </div>
</template>

<style lang="scss" scoped>
.uploadInput {
  label {
    width: 100%;
  }
}

.uploadedFiles {
  max-height: 15em;
  overflow-y: scroll;
}

.drop-area {
  padding-top: 3em;
  padding-bottom: 3em;
  border: 2px dashed #ccc;
  &.drag-on {
    background-color: #eee;
  }
}
</style>


<script>
export default {
  name: 'manage-newsite-view',
  created: function() {

  },
  data: () => {
    return {
      form: {
        siteType: 'OneOff',
        email: '',
        slug: '',
        food: null,
        checked: false,
        files: []
      },
      dragHover: false,
      siteTypeOptions: [
        { text: 'One Off', value: 'OneOff' },
        { text: 'Series', value: 'Series' },
      ],
      foods: [
        { text: 'Select One', value: null },
        'Carrots', 'Beans', 'Tomatoes', 'Corn'
      ],
      filesTableFields: ["name", "size", "progress"]
    }
  },
  methods: {
    newFile(v) {
      console.log(v)
      console.log(this.form.files)
    },
    onSubmit(e) {
      e.preventDefault();
      console.log(this.$refs.files)
    },
    formatSlug(value, e) {
      return value.toLowerCase().trim().replace(/\s+/g, "-").replace(/[^0-9a-zA-Z-]/g, '')
    },
    selectFiles(e) {
      console.log(e.target.webkitEntries)
      console.log(this.$refs.files.webkitEntries)
    }
  }
}
</script>
