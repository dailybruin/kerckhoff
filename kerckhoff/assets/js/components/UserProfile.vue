<template>
  <div class="container mt-3">
    <h2>Hello {{first_name}},</h2>
    <div class="row mt-3">
      <div class="col col-md-4">
        <img v-if="profile_img === ''" class="img-fluid rounded" src="/static/img/placeholder.png">
        <p v-if="email">{{email}}</p>
        <ul class="mt-4">
          <li>
            <a href="#">Upload New</a>
          </li>
          <li>
            <a href="/accounts/logout">Logout</a>
          </li>
        </ul>
      </div>
      <div class="col">
        <p>Commodo esse commodo eu id laboris sunt ullamco exercitation consectetur eu eiusmod. Reprehenderit et et adipisicing non minim duis elit ad laboris dolore aliquip dolor. Nisi cillum voluptate esse veniam reprehenderit fugiat voluptate eiusmod aliqua. Elit ad sit minim excepteur in laborum occaecat. Aliquip aute ut pariatur elit ullamco nisi commodo pariatur enim irure pariatur consectetur mollit. Ad deserunt dolore fugiat non esse officia nulla ad dolore do fugiat irure.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { axios, utils } from "../util";

export default {
  data: function() {
    return {
      first_name: "",
      email: "",
      profile_img: "",
      github_url: "",
      linkedin_url: ""
    };
  },
  beforeMount: function() {
    axios.get("/api/v2/userProfile/6/?format=json").then(res => {
      this.first_name = res.data.first_name;
      this.email = res.data.email;
      this.profile_img = res.data.profile_img;
      this.github_url = res.data.github_url;
      this.linkedin_url = res.data.linkedin_url;
      console.log(info);
    });
  }
};
</script>
