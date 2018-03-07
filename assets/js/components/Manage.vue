<template>
<div class="container mt-2">
  <div class="row mb-2">
    <div class="col col-sm-12">
      <h1 class="mt-2">Sites Manager</h1>
    </div>
  </div>
  <div class="row mb-3">
    <div class="col col-md-2">
      <b-list-group>
        <b-list-group-item to="/manage/packages">Packages</b-list-group-item>
        <b-list-group-item to="/manage/pages" >Static Sites</b-list-group-item>
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
