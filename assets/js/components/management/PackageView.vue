<template>
  <div class="container">
    <div class="row">
      <h2>
        {{ $route.params.slug }}
        <b-button class="ml-2" size="sm" variant="secondary">
          Update from GDrive
        </b-button>
      </h2>
    </div>
  </div>
</template>

<script>
export default {
  name: 'package-view'
}
</script>
