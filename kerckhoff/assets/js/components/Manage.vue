<template>
  <div class="container-fluid mt-2">
    <div class="row mb-2">
      <div class="col col-sm-12">
        <h1 class="mt-2">Sites Manager</h1>
      </div>
    </div>
    <div class="row mb-3">
      <div class="col col-md-2">
        <b-list-group>
          <b-list-group-item to="/manage/packages">Packages</b-list-group-item>
          <b-list-group-item href="#" disabled>Static Sites</b-list-group-item>
        </b-list-group>
      </div>
      <div class="col col-md-10">
        <keep-alive include="manage-display-view">
          <router-view></router-view>
        </keep-alive>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "manage-view"
};
</script>
