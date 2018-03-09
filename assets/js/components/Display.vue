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
</div>
</template>

<style lang="scss" scoped>

.wip-bear {
  max-width: 700px;
}

.wip-text {
  text-align: center;
}

</style>


<script>
export default {
  name: 'display-view',
  data: function () {
    /*this.$http.get("http://localhost:5000/pages?pagesPerQuery=50&queryNumber=1", function(data) {
      alert("hel");
    });*/
    return {
      todos: [
        { text: 'Learn Vue' },
        { text: 'Learn Docker' },
        { text: 'Learn Everything' }
      ]
    }
  }
}
</script>
