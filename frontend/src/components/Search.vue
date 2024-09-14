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
import { useRouter } from 'vue-router'
import debounce from 'lodash/debounce'

export default {
  name: 'Search',
  setup() {
    const store = useStore()
    const router = useRouter()
    const searchQuery = ref('')

    const search = () => {
      store.dispatch('performSearch', searchQuery.value)
      router.push({ name: 'SearchResults', query: { q: searchQuery.value } })
    }

    const debouncedSearch = debounce(search, 300)

    onMounted(() => {
      // Perform an initial search when the component is mounted
      search()
    })

    return {
      searchQuery,
      debouncedSearch
    }
  }
}
</script>