<template>
  <div class="main">
    <Navbar />
    <router-view></router-view>
    <PageFoot />
  </div>
</template>

<script>
import Navbar from './components/Navbar'
import PageFoot from './components/Footer'
import Profile from './components/UserProfile'

export default {
  props: ['type'],
  components: {
    Navbar,
    PageFoot,
    Profile
  },
  name: 'mainModule'
}
</script>
