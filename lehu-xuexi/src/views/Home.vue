<template>
  <div class="home">
    <HelloWorld msg="DRF个人博客" />
    <img alt="Vue logo" src="../assets/drf.png" style="width:1000px;height:500px">
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  components: {
    HelloWorld
  }
}
</script>

<style scoped>
  .home{
    text-align: center;
  }
</style>
