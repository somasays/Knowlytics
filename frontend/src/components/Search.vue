<template>
  <div class="search-container">
    <input
      v-model="searchQuery"
      @input="debouncedSearch"
      type="text"
      placeholder="Search data products..."
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import debounce from 'lodash/debounce'

export default {
  name: 'Search',
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    const searchQuery = ref('')

    onMounted(() => {
      const query = route.query.q || ''
      searchQuery.value = query
    })

    const search = () => {
      const query = searchQuery.value.trim()
      if (query) {
        store.dispatch('performSearch', { query, append: false })
        router.push({ name: 'SearchResults', query: { q: query } })
      } else {
        store.commit('resetSearch')
      }
    }

    const debouncedSearch = debounce(search, 300)

    return {
      searchQuery,
      debouncedSearch
    }
  }
}
</script>

<style scoped lang="scss">
.search-container {
  /* Existing styles */
}
</style>