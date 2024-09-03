import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    searchResults: [],
    searchLoading: false,
    searchError: null,
    searchPerformed: false,
  },
  mutations: {
    setSearchResults(state, results) {
      state.searchResults = results
      state.searchPerformed = true
    },
    setSearchLoading(state, isLoading) {
      state.searchLoading = isLoading
    },
    setSearchError(state, error) {
      state.searchError = error
      state.searchPerformed = true // Added this line
    },
    // Added this mutation
    resetSearch(state) {
      state.searchResults = []
      state.searchError = null
      state.searchPerformed = false
    },
  },
  actions: {
    async performSearch({ commit }, query) {
      console.log('Action: performSearch initiated with query:', query)
      commit('setSearchLoading', true)
      commit('resetSearch') // Added this line
      try {
        console.log('Sending API request to:', '/api/v1/search')
        const response = await axios.get('/api/v1/search', { // Changed from '/api/search'
          params: { query }
        })
        console.log('API response received:', response)
        console.log('Search results:', response.data.results)
        commit('setSearchResults', response.data.results)
        // if (response.data.results.length > 0) {
        //   await router.push('/search')
        // }
      } catch (error) {
        console.error('Error performing search:', error)
        commit('setSearchError', 'An error occurred while searching. Please try again.')
      } finally {
        commit('setSearchLoading', false)
      }
    }
  },
})