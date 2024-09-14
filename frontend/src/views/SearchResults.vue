<template>
  <div class="search-results" @scroll="handleScroll" ref="scrollContainer">
    <div v-if="searchLoading && searchResults.length === 0" class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      Loading...
    </div>
    <div v-else-if="searchError" class="error-message">
      <i class="fas fa-exclamation-circle"></i>
      {{ searchError }}
    </div>
    <div v-else-if="searchResults.length > 0" class="results-list">
      <div v-for="result in searchResults" :key="result.id" class="result-item">
        <h3>{{ result.source.name || result.source.term }}</h3>
        <p>{{ result.source.description || result.source.definition }}</p>
        <span class="result-type">Type: {{ result.type }}</span>
      </div>
      <div v-if="hasMore" class="loading">
        <i class="fas fa-spinner fa-spin"></i>
        Loading more results...
      </div>
    </div>
    <div v-else-if="searchPerformed" class="no-results">
      <i class="fas fa-search"></i>
      <p>No results found for your search query.</p>
      <p>Try adjusting your search terms or explore our suggested topics.</p>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'SearchResults',
  setup() {
    const store = useStore()
    const scrollContainer = ref(null)

    const searchResults = computed(() => store.state.searchResults)
    const searchLoading = computed(() => store.state.searchLoading)
    const searchError = computed(() => store.state.searchError)
    const searchPerformed = computed(() => store.state.searchPerformed)
    const hasMore = computed(() => store.state.hasMore)
    const currentQuery = computed(() => store.state.currentQuery)

    const loadMore = () => {
      if (!store.state.searchLoading && store.state.hasMore) {
        store.dispatch('performSearch', { query: currentQuery.value, append: true })
      }
    }

    const handleScroll = () => {
      const container = scrollContainer.value
      if (container) {
        const scrollThreshold = 300
        if (container.scrollTop + container.clientHeight >= container.scrollHeight - scrollThreshold) {
          loadMore()
        }
      }
    }

    onMounted(() => {
      const query = new URLSearchParams(window.location.search).get('q') || ''
      if (query) {
        store.dispatch('performSearch', { query, append: false })
      }
    })

    return {
      searchResults,
      searchLoading,
      searchError,
      searchPerformed,
      hasMore,
      handleScroll,
      scrollContainer
    }
  }
}
</script>

<style scoped lang="scss">
.search-results {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 80vh;
  overflow-y: auto;

  .loading, .error-message, .no-results {
    text-align: center;
    padding: 40px 20px;
    color: #6c757d;
  }

  .loading i {
    font-size: 48px;
    margin-bottom: 20px;
  }

  .error-message {
    color: #721c24;
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
  }

  .results-list {
    .result-item {
      margin-bottom: 20px;
      padding: 15px;
      background-color: #f9f9f9;
      border-radius: 4px;

      h3 {
        margin-top: 0;
        color: #007bff;
      }

      .result-type {
        font-size: 0.8em;
        color: #6c757d;
      }
    }

    .loading {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }
  }

  .no-results {
    text-align: center;
    padding: 40px 20px;
    color: #6c757d;
  }
}
</style>
