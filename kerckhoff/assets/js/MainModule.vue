<template>
  <div class="main">
    <Navbar v-bind:authenticated="isAuthenticated"/>
    <router-view></router-view>
    <PageFoot />
  </div>
</template>

<script>
import Navbar from "./components/Navbar";
import PageFoot from "./components/Footer";
import Profile from "./components/UserProfile";

export default {
  props: ["type"],
  components: {
    Navbar,
    PageFoot,
    Profile
  },
  computed: {
    isAuthenticated: function() {
      return this.$router.currentRoute.fullPath.includes("/manage/");
    }
  },
  name: "mainModule"
};
</script>
