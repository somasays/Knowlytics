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
      state.searchPerformed = true
    },
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
      commit('resetSearch')
      try {
        const response = await axios.get('/api/v1/search', {
          params: { query }
        })
        console.log('API response received:', response)
        if (response.data && response.data.results) {
          commit('setSearchResults', response.data.results)
        } else {
          commit('setSearchResults', [])
        }
      } catch (error) {
        console.error('Error performing search:', error)
        commit('setSearchError', 'An error occurred while searching. Please try again.')
      } finally {
        commit('setSearchLoading', false)
      }
    }
  },
})