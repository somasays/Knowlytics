<template>
  <header>
    <div class="header-content">
      <SearchBar class="search-bar" />
      <div class="right-options">
        <button class="icon-button" title="Notifications"><i class="fa fa-bell"></i></button>
        <button class="icon-button" title="Help"><i class="fa fa-question-circle"></i></button>
        <div class="user-profile">
          <img src="../assets/user-avatar.png" alt="User" />
          <span>Somasundaram</span>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import SearchBar from './SearchBar.vue'

export default {
  name: 'AppHeader',
  components: {
    SearchBar
  }
}
</script>

<style scoped lang="scss">
header {
  width: 100%;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 12px 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  max-width: 100%;
  margin: 0 auto;
}

.search-bar {
  flex-grow: 1;
  max-width: none;
  margin-right: 24px;
}

.right-options {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;

  .icon-button {
    background-color: transparent;
    border: none;
    font-size: 18px;
    color: #2c3e50;
    cursor: pointer;
    padding: 8px;
    border-radius: 50%;
    transition: background-color 0.3s;

    &:hover {
      background-color: #f0f2f5;
    }
  }

  .user-profile {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 20px;
    transition: background-color 0.3s;

    &:hover {
      background-color: #f0f2f5;
    }

    img {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      margin-right: 8px;
    }

    span {
      font-weight: 500;
      font-size: 14px;
    }
  }
}
</style>