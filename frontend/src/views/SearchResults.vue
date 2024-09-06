<template>
  <div class="search-results">
    <div v-if="searchLoading" class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      Searching...
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
    </div>
    <div v-else-if="searchPerformed" class="no-results">
      <i class="fas fa-search"></i>
      <p>No results found for your search query.</p>
      <p>Try adjusting your search terms or explore our suggested topics.</p>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'SearchResults',
  setup() {
    const store = useStore()

    return {
      searchResults: computed(() => store.state.searchResults),
      searchLoading: computed(() => store.state.searchLoading),
      searchError: computed(() => store.state.searchError),
      searchPerformed: computed(() => store.state.searchPerformed)
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

  .loading, .error-message, .no-results {
    text-align: center;
    padding: 40px 20px;
    color: #6c757d;
  }

  .loading i, .error-message i, .no-results i {
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
  }
}
</style>
