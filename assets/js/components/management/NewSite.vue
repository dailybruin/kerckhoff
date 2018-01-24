<template>
  <div class="example-drag">
    <div class="upload">
      <ul v-if="files.length">
        <li v-for="(file, index) in files" :key="file.id">
          <span>{{file.name}}</span> -
          <span>{{file.size}}</span> -
          <span>{{file.s3_state}}</span>
          <span v-if="file.error">{{file.error}}</span>
          <span v-else-if="file.success">success</span>
          <span v-else-if="file.active">active</span>
          <span v-else-if="file.active">active</span>
          <span v-else></span>
        </li>
      </ul>
      <ul v-else>
        <td colspan="7">
          <div class="text-center p-5">
            <h4>Drop files anywhere to upload<br/>or</h4>
            <label for="file" class="btn btn-lg btn-primary">Select Files</label>
          </div>
        </td>
      </ul>

      <div v-show="$refs.upload && $refs.upload.dropActive" class="drop-active">
    		<h3>Drop files to upload</h3>
      </div>

      <div class="example-btn">
        <file-upload
          class="btn btn-primary"
          post-action="/upload/post"
          :multiple="true"
          :drop="true"
          :drop-directory="true"
          v-model="files"
          @input-file="inputFile"
          ref="upload">
          <i class="fa fa-plus"></i>
          Select files
        </file-upload>
        <button type="button" class="btn btn-success"
          v-if="readyForUpload && (!$refs.upload || !$refs.upload.active) "
          @click.prevent="$refs.upload.active == true">
          <i class="fa fa-arrow-up" aria-hidden="true"></i>
          Start Upload
        </button>
      </div>

      <br/>
      <div class="progresss-bar">
        <h5>Progress:<br/></h5>
        <b-progress :value="progress" variant="info" :max="max" show-progress animated></b-progress>
      </div>

    </div>

  </div>
</template>
<style>
.example-drag label.btn {
  margin-bottom: 0;
  margin-right: 1rem;
}


.example-drag .drop-active {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  position: fixed;
  z-index: 9999;
  opacity: .6;
  text-align: center;
  background: #000;
}

.example-drag .drop-active h3 {
  margin: -.5em 0 0;
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  -webkit-transform: translateY(-50%);
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
  font-size: 40px;
  color: #fff;
  padding: 0;
}
</style>

<script>
import FileUpload from 'vue-upload-component'
export default {
  components: {
    FileUpload,
  },

  computed: {
    readyForUpload: function() {
      return this.files.length !== 0 && this.files.filter(f => f.s3_state === "NOT READY").length === 0
    }
  },

  methods: {
    inputFile: function (newFile, oldFile) {
      if (newFile && !oldFile) {
        console.log("adding a new file, getting stuff")
        console.log(newFile.file)
        this.getSignedRequest(newFile)
      }
      if (newFile && oldFile && !newFile.active && oldFile.active) {
        // Get response data
        console.log('response', newFile.response)
        if (newFile.xhr) {
          //  Get the response status code
          console.log('status', newFile.xhr.status)
        }
      }
    },

    uploadFile(file, s3Data, url) {
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

    getSignedRequest(newFile){
      const file = newFile.file
      const xhr = new XMLHttpRequest();
      this.$set(newFile, 's3_state', 'NOT READY')
      xhr.open('GET', `/api/sign-s3?file_name=${file.name}&file_type=${file.type}`);
      xhr.onreadystatechange = () => {
        if(xhr.readyState === 4){
          if(xhr.status === 200){
            const response = JSON.parse(xhr.responseText);
            newFile.s3_state = "READY"
            //uploadFile(file, response.data, response.url);
          }
          else{
            alert('Could not get signed URL.');
          }
        }
      };
      xhr.send();
    },

    initUpload(){
      console.log("Sfdsdfsdfdfsdf")
      const files = document.getElementById('file-input').files;
      const file = files[0];
      if(!file){
        return alert('No file selected.');
      }
      getSignedRequest(file);
    }

  },



  data() {
    return {
      files: [],
      max: 100,
      progress: 33
    }
  }

}
</script>
