<template>
  <div>
    <h2 class="mb-3">New Site - TESTING KAI's EDITS</h2>



    <input type="file" id="file-input">
    <p id="status">Please select a file</p>
    <img style="border:1px solid gray;width:300px;" id="preview" src="/static/media/default.png">

    <h2>Your information</h2>

    <form method="POST" action="/submit-form/">
      <input type="hidden" id="avatar-url" name="avatar-url" value="/static/media/default.png">
      <input type="text" name="username" placeholder="Username"><br>
      <input type="text" name="full-name" placeholder="Full name"><br><br>

      <hr>
      <h2>Save changes</h2>

      <input type="submit" value="Update profile">
    </form>



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


<script type="text/javascript">
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
    },



    uploadFile(file, s3Data, url){
      const xhr = new XMLHttpRequest();
      xhr.open('POST', s3Data.url);
      xhr.setRequestHeader('x-amz-acl', 'public-read');
      const postData = new FormData();
      for(key in s3Data.fields){
        postData.append(key, s3Data.fields[key]);
      }
      postData.append('file', file);
      xhr.onreadystatechange = () => {
        if(xhr.readyState === 4){
          if(xhr.status === 200 || xhr.status === 204){
            document.getElementById('preview').src = url;
            document.getElementById('avatar-url').value = url;
          }
          else{
            alert('Could not upload file.');
          }
        }
      };
      xhr.send(postData);
    },




    getSignedRequest(file){
      const xhr = new XMLHttpRequest();
      xhr.open('GET', `/sign-s3?file-name=${file.name}&file-type=${file.type}`);
      xhr.onreadystatechange = () => {
        if(xhr.readyState === 4){
          if(xhr.status === 200){
            const response = JSON.parse(xhr.responseText);
            uploadFile(file, response.data, response.url);
          }
          else{
            alert('Could not get signed URL.');
          }
        }
      };
      xhr.send();
    },
    

    initUpload(){
      const files = document.getElementById('file-input').files;
      const file = files[0];
      if(!file){
        return alert('No file selected.');
      }
      getSignedRequest(file);
    }






 } 
}
</script>
