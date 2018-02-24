<template>
<div class="container mt-3">
  <h2>Display view!</h2>
  {{todos}}
</div>
</template>

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
