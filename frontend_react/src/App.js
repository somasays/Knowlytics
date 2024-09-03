import React from 'react';
import Layout from './components/Layout';
import Search from './components/Search';

function App() {
  const handleSearchResults = (callback) => {
    return (query, results) => {
      console.log("App: handleSearchResults called", { query, results });
      callback(query, results);
    };
  };

  return (
    <Layout>
      <Search onSearchResults={handleSearchResults} />
    </Layout>
  );
}

export default App;