import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    searchResults: [],
    searchLoading: false,
    searchError: null,
    searchPerformed: false,
    currentPage: 1,
    pageSize: 20,
    hasMore: true,
    currentQuery: ''
  },
  mutations: {
    setSearchResults(state, results) {
      state.searchResults = results
      state.searchPerformed = true
    },
    appendSearchResults(state, results) {
      state.searchResults = [...state.searchResults, ...results]
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
      state.currentPage = 1
      state.hasMore = true
      state.currentQuery = ''
    },
    setCurrentQuery(state, query) {
      state.currentQuery = query
    },
    setHasMore(state, hasMore) {
      state.hasMore = hasMore
    },
    incrementPage(state) {
      state.currentPage += 1
    }
  },
  actions: {
    async performSearch({ commit, state }, { query, append = false }) {
      if (!append) {
        commit('resetSearch')
        commit('setCurrentQuery', query)
      }
      commit('setSearchLoading', true)
      try {
        const response = await axios.get('/api/v1/search', {
          params: {
            query: query,
            page: state.currentPage,
            size: state.pageSize
          }
        })
        const results = response.data.results
        if (append) {
          commit('appendSearchResults', results)
        } else {
          commit('setSearchResults', results)
        }
        commit('setHasMore', results.length === state.pageSize)
        if (append) {
          commit('incrementPage')
        }
      } catch (error) {
        commit('setSearchError', 'An error occurred while fetching search results.')
      } finally {
        commit('setSearchLoading', false)
      }
    }
  },
  modules: {
  }
})