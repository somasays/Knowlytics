<template>
  <div class="search-bar">
    <select v-model="selectedType">
      <option value="all">All</option>
      <!-- Add more options as needed -->
    </select>
    <div class="search-input-wrapper">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Search for Data Assets" 
        @keyup.enter="performSearch"
      />
      <button class="search-icon" @click="performSearch">
        <i class="fas fa-search"></i>
      </button>
    </div>
    <button class="icon-button"><i class="fas fa-th"></i></button>
    <button class="icon-button" title="Advanced Options"><i class="fas fa-cog"></i></button>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'SearchBar',
  setup() {
    const store = useStore()
    const router = useRouter()
    const selectedType = ref('all')
    const searchQuery = ref('')

    const performSearch = async () => {
      console.log('Initiating search with query:', searchQuery.value)
      await store.dispatch('performSearch', searchQuery.value)
      await router.push('/search')
    }

    return {
      selectedType,
      searchQuery,
      performSearch
    }
  }
}
</script>
<style scoped lang="scss">
.search-bar {
  display: flex;
  align-items: center;
  background-color: #f1f3f5;
  border-radius: 4px;
  padding: 8px;
  width: 100%;

  select, input {
    border: none;
    background: transparent;
    font-size: 16px;
  }

  select {
    padding: 5px;
    margin-right: 10px;
  }

  .search-input-wrapper {
    position: relative;
    flex-grow: 1;
    display: flex;
    align-items: center;

    input {
      width: 100%;
      padding: 8px;
      padding-right: 40px;
    }

    .search-icon {
      position: absolute;
      right: 8px;
      background: none;
      border: none;
      cursor: pointer;
      font-size: 18px;
      color: #6c757d;
      transition: color 0.3s ease;

      &:hover {
        color: #007bff;
      }
    }
  }

  .icon-button {
    background: none;
    border: none;
    cursor: pointer;
    margin-left: 10px;
    font-size: 18px;
    color: #6c757d;
    transition: color 0.3s ease;

    &:hover {
      color: #007bff;
    }
  }
}
</style>