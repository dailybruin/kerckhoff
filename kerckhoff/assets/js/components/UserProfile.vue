<template>
<div class="container mt-3">
  <h2>Hello {{userInfo.first_name}},</h2>
  <div class="row mt-3">
    <div class="col col-md-4">
      <img v-if="userInfo.profile_img === ''" class="img-fluid rounded" src="/static/img/placeholder.png" />
      <ul class="mt-4">
        <li><a href="/accounts/logout">Upload New</a></li>
        <li><a href="/accounts/logout">Logout</a></li>
      </ul>
    </div>
    <div class="col">
      <p>Commodo esse commodo eu id laboris sunt ullamco exercitation consectetur eu eiusmod. Reprehenderit et et adipisicing non minim duis elit ad laboris dolore aliquip dolor. Nisi cillum voluptate esse veniam reprehenderit fugiat voluptate eiusmod aliqua. Elit ad sit minim excepteur in laborum occaecat. Aliquip aute ut pariatur elit ullamco nisi commodo pariatur enim irure pariatur consectetur mollit. Ad deserunt dolore fugiat non esse officia nulla ad dolore do fugiat irure.</p>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'user-profile',
  data: function() {
    return {
      userInfo: info
    }
  }
}
</script>
