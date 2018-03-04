<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="exampleInputGroup1"
                    label="Email address:"
                    label-for="exampleInput1"
                    description="We'll never share your email with anyone else.">
        <b-form-input id="exampleInput1"
                      type="email"
                      v-model="form.email"
                      required
                      placeholder="Enter email">
        </b-form-input>
      </b-form-group>

      <!-- Chooses whether the page is a one off or part of a series -->
      <b-button variant="outline-success" :pressed.sync="myToggle" > One Off </b-button>
      <b-button variant="outline-success" :pressed.sync="myToggle" > Series </b-button>

      <!-- Input field for title of the work -->
      <b-form-group id="exampleInputGroup2"
                    label="Title:"
                    label-for="exampleInput2">
        <b-form-input id="exampleInput2"
                      type="text"
                      v-model="form.name"
                      required
                      placeholder="Enter name">
        </b-form-input>
      </b-form-group>

      <!-- Input field for the contributors-->
      <b-form-group id="exampleInputGroup3"
                    label="Food:"
                    label-for="exampleInput3">
        <b-form-select id="exampleInput3"
                      :options="type"
                      required
                      v-model="form.food">
        </b-form-select>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </div>
</template>

<style lang="scss" scoped>
.footer {
  margin-top: 5em;
}

</style>


<script>
  import FileUpload from 'vue-upload-component'
  export default {
    data () {
      return {
        form: {
          email: '',
          name: '',
          food: null,
          checked: []
        },
        type: [
          { text: 'Select One', value: null },
          'Series', 'One-off'
        ],
        show: true,
        myToggle: false
      }
    },
      computed: {
        btnStates () {
          return "success"
        }
      }
    }
  }
</script>
