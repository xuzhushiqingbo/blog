<template>
  <div id="app">
    <Row>
      <i-col :span="2"><div style="width: 100%;height: 1px"></div></i-col>
      <i-col :span="20">
        <div id="nav">
          <top-nav></top-nav>
        </div>
        <div id="container">
          <router-view/>
        </div>
      </i-col>
      <i-col :span="2"><div style="width: 100%;height: 1px"></div></i-col>
    </Row>
  </div>
</template>

<script>
import TopNav from './views/TopNav'
export default {
  name: 'APP',
  components: { TopNav }
}
</script>
<style lang="less">
  #app {
    /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
    /*-webkit-font-smoothing: antialiased;*/
    /*-moz-osx-font-smoothing: grayscale;*/
    /*text-align: center;*/
    /*color: #2c3e50;*/
  }
  #nav {
    margin-bottom: 8px;
  }
  #container {
    background: rgba(206, 206, 206, 0.38);
    min-height: 1000px;
  }
</style>
