<template>
<div class="container mt-5">
  <div class="row justify-content-center align-items-center">
    <img class="wip-bear" src="/static/img/wip_bear.png" />
  </div>
  <div class="wip-text">
    <h1>You have found a WIP!</h1>
    <p>This is the future home of the Daily Bruin's online projects! <br /> The platform is <a target="_blank" href="https://github.com/daily-bruin/kerckhoff">still a work in progress</a>, but if you are here <strong>on business</strong>...</p>
    <p>You can proceed on <a href="/manage">here</a>.</p>
  </div>
  <br />
  <h1>WIP: Pages Masonry View</h1>
  <div>
    <ul>
      <li v-for="page of pages">
        {{page.title}}
      </li>
    </ul>
  </div>

  <div v-masonry transition-duration="0.3s" item-selector=".pageBlock">
    <div v-masonry-tile class="pageBlock" v-for="page of pages">
      <!--img class="wip-bear" src="/static/img/wip_bear.png" /-->
      <p>{{page.title}}</p>
    </div>
  </div>

</div>
</template>

<style lang="scss" scoped>

.wip-bear {
  max-width: 700px;
}

.wip-text {
  text-align: center;
}

/*
.pageBlock {
  margin-bottom:  0;
}

*/

</style>


<script>
import {axios} from "../util";

export default {
  name: 'display-view',
  data: function () {
    return {
      pages: []
    }
  },

  created() {
    axios.get(`/pages?pagesPerQuery=50&queryNumber=1`).then(response => {
      this.pages = response.data
    })
  }
}
</script>
