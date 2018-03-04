<template>
<div class="container mt-2">
  <div class="row mb-2">
    <div class="col col-sm-12">
      <h1 class="mt-2">Pages</h1>
    </div>
  </div>
  <div class="container">
    <div class="row mb-2">
      <h4 class="mt-0">Random site 1</h4>
    </div>
    <div class="row mb-2">
      <h4 class="mt-0">Random site 2</h4>
    </div>
    <div class="row mb-2">
      <h4 class="mt-0">Random site 3</h4>
    </div>
  </div>
  <div class="row mb-3">
    <div class="col col-md-2">
      <b-list-group>
        <b-list-group-item to="/manage/pages/new">Upload</b-list-group-item>
      </b-list-group>
    </div>
    <div class="col col-md-10">
      <router-view></router-view>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'manage-view'
}
</script>
