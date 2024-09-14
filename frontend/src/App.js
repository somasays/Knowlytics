import React from 'react';
import Layout from './components/Layout';
import Search from './components/Search';

function App() {
  const handleSearchResults = (callback) => {
    return async (query) => {
      console.log("App: handleSearchResults called", { query });
      const results = await fetchSearchResults(query);
      callback(query, results);
    };
  };

  const fetchSearchResults = async (query) => {
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    return await response.json();
  };

  return (
    <Layout>
      <Search onSearchResults={handleSearchResults} />
    </Layout>
  );
}

export default App;