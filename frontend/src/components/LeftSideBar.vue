<template>
  <div class="left-sidebar">
    <router-link to="/" class="logo">
      <img src="../assets/logo.png" alt="Knowlytics" />
    </router-link>
    <nav>
      <a v-for="(item, index) in navItems" :key="index" :href="item.link" :title="item.name">
        <i :class="item.icon"></i>
        <span class="icon-text">{{ item.name }}</span>
      </a>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'LeftSideBar',
  data() {
    return {
      navItems: [
        { name: 'Home', icon: 'fas fa-home', link: '/' },
        { name: 'Search', icon: 'fas fa-search', link: '/search' },
        { name: 'Notifications', icon: 'fas fa-bell', link: '/notifications' },
        { name: 'Globe', icon: 'fas fa-globe', link: '/globe' },
        { name: 'Catalog', icon: 'fas fa-book', link: '/catalog' },
        { name: 'Dictionary', icon: 'fas fa-book-open', link: '/dictionary' }
      ]
    }
  }
}
</script>

<style scoped lang="scss">
.left-sidebar {
  width: auto;
  min-width: 80px;
  background-color: #2c3e50;
  color: #ecf0f1;
  padding: 20px 10px;
  display: flex;
  flex-direction: column;
  height: 100vh;
  box-sizing: border-box;
  flex-shrink: 0;
  transition: min-width 0.3s ease;

  &:hover {
    min-width: 240px;

    .icon-text {
      display: inline;
    }
  }

  .logo {
    margin-bottom: 30px;
    text-align: center;
    
    img {
      width: 60px;
      transition: width 0.3s ease;
    }
  }

  nav {
    display: flex;
    flex-direction: column;

    a {
      color: #ecf0f1;
      text-decoration: none;
      padding: 12px 15px;
      margin-bottom: 10px;
      border-radius: 5px;
      transition: background-color 0.3s;
      display: flex;
      align-items: center;

      &:hover {
        background-color: #34495e;
      }

      i {
        font-size: 20px;
        width: 30px;
        text-align: center;
      }

      .icon-text {
        display: none;
        margin-left: 10px;
        transition: opacity 0.3s ease;
      }
    }
  }

  &:hover {
    .logo img {
      width: 120px;
    }
  }
}
</style>