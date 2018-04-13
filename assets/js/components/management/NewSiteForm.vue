<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="titleGroup"
                    label="Title:"
                    label-for="titleInput">
        <b-form-input id="titleInput"
                      type="text"
                      v-model="form.title"
                      required
                      placeholder="Enter Title">
        </b-form-input>
      </b-form-group>

      <b-form-group id="slugGroup"
                    label="Slug ID:"
                    label-for="slugInput">
        <b-form-input id="slugInput"
                      type="text"
                      v-model="form.slug"
                      required
                      placeholder="Enter Slug ID">
        </b-form-input>
      </b-form-group>

      <b-form-group id="typeGroup"
                    label="Type:"
                    label-for="typeInput">
        <b-form-select id="typeInput"
                       v-model="selected"
                       required>
            <option value="item1">One-shot Page</option>
            <option value="item2">Series Page</option>
        </b-form-select>
      </b-form-group>

      <!--Adding conditional if the series is selected-->

      <div id="hidden" style="display: none">
        <template>
          <b-form-group id="seriesGroup"
                        label="Series Elements:"
                        label-for="seriesInput"
                        >
            <b-form-input id="seriesInput"
                          type="text"
                          v-model="form.series"
                          required
                          placeholder="">
            </b-form-input>
          </b-form-group>
        </template>
      </div>


      <b-form-group id="dateGroup"
                    label="Published Date:"
                    label-for="dateInput">
        <b-form-input id="dateInput"
                      type="date"
                      required
                      v-model="form.date">
        </b-form-input>
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
        title: '',
        slug: '',
        selected: ''
        //no comma here on the last line
      },
      show: true
    }
  }
}
</script>
