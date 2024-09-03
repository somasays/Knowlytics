<template>
  <div id="app">
    <LeftSideBar />
    <div class="main-content">
      <Header />
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import LeftSideBar from './components/LeftSideBar.vue'
import Header from './components/Header.vue'
export default {
  name: 'App',
  components: {
    LeftSideBar,
    Header
  }
}
</script>

<style lang="scss">
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f5f7fa;
}

#app {
  display: flex;
  height: 100vh;
  width: 100vw;
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  height: 100%;
  width: calc(100% - 80px);
  padding: 20px;
  box-sizing: border-box;
  transition: width 0.3s ease;
}

#app:hover .main-content {
  width: calc(100% - 240px);
}
</style>