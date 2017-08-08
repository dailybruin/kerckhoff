<template>
<div class="container mt-2">
  <div class="row mb-2">
    <div class="col col-sm-12">
      <h2>Site Manager</h2>
    </div>
  </div>
  <div class="row mb-3">
    <div class="col col-md-4">
      <b-button variant="primary" to="new">
        <icon class="align-middle" name="plus"></icon>
        <span class="align-middle ml-1">New Site</span>
      </b-button>
    </div>
    <div class="col">
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
