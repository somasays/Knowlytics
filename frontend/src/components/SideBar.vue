<template>
  <div id="app">
    <header>
      <div class="logo">
        <h1>Knowlytics</h1>
      </div>
      <SearchBar />
      <UserMenu />
    </header>
    <div class="main-content">
      <SideBar />
      <router-view></router-view>
      <RightSideBar />
    </div>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue'
import UserMenu from './components/UserMenu.vue'
import SideBar from './components/SideBar.vue'
import RightSideBar from './components/RightSideBar.vue'

export default {
  name: 'App',
  components: {
    SearchBar,
    UserMenu,
    SideBar,
    RightSideBar
  }
}
</script>

<style lang="scss">
#app {
  font-family: Arial, sans-serif;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: linear-gradient(90deg, #007bff, #0056b3);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo h1 {
  margin: 0;
  font-size: 2em;
}

.main-content {
  display: flex;
  padding: 20px;
  background-color: #f0f2f5;
}
</style>