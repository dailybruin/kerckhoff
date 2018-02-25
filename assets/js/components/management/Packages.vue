<template>
<div class="container">
  <div class="col">
    <b-button-group>
      <b-button v-b-modal.create-modal variant="primary">
        <icon class="align-middle" name="plus"></icon>
        <span class="align-middle ml-1">New Package</span>
      </b-button>
      <b-button>
        <icon class="align-middle" name="refresh"></icon>
      </b-button>
    </b-button-group>
  </div>

  <b-modal id="create-modal" size="lg" title="New Package" ref="createModal">
    <b-form ref="packageForm" @submit="submitForm">
      <div class="container" fluid>
          <b-form-group id="slug-label"
                        label="Package Slug:"
                        label-for="slug-input"
                        description="The article slug (e.g. sports.mbb.oregon)">
            <b-form-input id="slug-input"
                          type="text"
                          :state="errs.slug == null ? null : false"
                          v-model="form.slug"
                          required
                          placeholder="Enter package slug">
            </b-form-input>
            <b-form-invalid-feedback v-if="errs.slug">
              {{errs.slug[0]}}
            </b-form-invalid-feedback>
          </b-form-group>

          <b-form-group id="desc-label"
                        label="Package Description:"
                        label-for="desc-input"
                        description="A brief description of the package.">
            <b-form-input id="desc-input"
                          type="text"
                          :state="errs.description == null ? null : false"
                          v-model="form.description"
                          required
                          placeholder="Enter package description">
            </b-form-input>
            <b-form-invalid-feedback v-if="errs.description">
              {{errs.description[0]}}
            </b-form-invalid-feedback>
          </b-form-group>

          <b-form-group id="url-label"
                        label="Package Google Drive URL:"
                        label-for="url-input"
                        description="(Optional) Link to the Google drive folder (inside the Repo folder) if it has already been created. We'll create the folder for you if this is left blank.">
            <b-form-input id="url-input"
                          type="url"
                          :state="errs.drive_folder_url == null ? null : false"
                          v-model="form.drive_folder_url"
                          placeholder="Enter Google Drive URL">
            </b-form-input>
            <b-form-invalid-feedback v-if="errs.drive_folder_url">
              {{errs.drive_folder_url[0]}}
            </b-form-invalid-feedback>
          </b-form-group>

          <b-form-group id="date-label"
                        label="Publish Date:"
                        label-for="date-input"
                        description="The package publishing date.">
            <b-form-input id="date-input"
                          type="date"
                          :state="errs.publish_date == null ? null : false"
                          v-model="form.publish_date">
            </b-form-input>
            <b-form-invalid-feedback  v-if="errs.publish_date">
              {{errs.publish_date[0]}}
            </b-form-invalid-feedback>
          </b-form-group>
      </div>
    </b-form>
    <div slot="modal-footer" class="w-100">
      <b-btn variant="primary" v-if="!submitted" @click="submitForm">
        Submit
      </b-btn>
      <h4 v-else>
        Creating...
      </h4>
    </div>
  </b-modal>

</div>
</template>

<script>
import {axios, utils} from "../../util";

export default {
  name: "manage-display-view",
  computed: {
    hasError: function() {
      for(let err in this.errs) {
        if(this.errs[err] != null)
          console.log("err")
          return true
      }
      console.log("no err")
      return false
    }
  },
  data() {
    return {
      form: {
        slug: "",
        description: "",
        drive_folder_url: "",
        publish_date: ""
      },
      errs: {
        slug: null,
        description: null,
        drive_folder_url: null,
        publish_date: null
      },
      submitted: false
    };
  },
  methods: {
    submitForm: function(evt) {
      //evt.preventDefault();
      // if(this.$refs.packageForm.$el.checkValidity() === false) {
      //   this.$refs.packageForm.validated = true

      // }
      // this.$refs.packageForm.validated = true
      console.log(this.form)
      this.submitted = true;
      let res = axios.post("/api/packages", this.form)
        .then((res) => {
          console.log(res)
          this.form = {
            slug: "",
            description: "",
            drive_folder_url: "",
            publish_date: ""
          }
          this.errs = {
            slug: null,
            description: null,
            drive_folder_url: null,
            publish_date: null
          }
          this.$refs.createModal.hide()
        })
        .catch((err) => {
          console.log(err.response);
          this.errs = err.response.data;
          this.submitted = false;
        })
    }
  }
};
</script>
