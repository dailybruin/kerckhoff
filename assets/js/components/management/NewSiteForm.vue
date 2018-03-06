<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="emailAddress"
                    label="Email address:"
                    label-for="emailAddress">
        <b-form-input id="emailAddress"
                      type="email"
                      v-model="form.email"
                      required
                      placeholder="Enter email">
        </b-form-input>
      </b-form-group>
      <b-form-group id="names"
                    label="Contributor Name:"
                    label-for="names">
        <b-form-input id="names"
                      type="text"
                      v-model="form.name"
                      required
                      placeholder="Enter name">
        </b-form-input>
      </b-form-group>
      <b-form-group id="typeInput"
                    label="Type:"
                    label-for="typeInput">
        <b-form-select id="typeInput"
                      :options="type"
                      required
                      v-model="form.type">
        </b-form-select>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      form: {
        email: '',
        name: '',
        type: null,
      },
      type: [
        { text: 'Select One', value: null },
        'One-off', 'Series'
      ],
      show: true
    }
  }
}
</script>
