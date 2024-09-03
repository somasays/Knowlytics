import React, { useState } from 'react';
import { TextField, Button, List, ListItem, ListItemText } from '@material-ui/core';
import axios from 'axios';

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/search?query=${query}`);
      setResults(response.data.results);
    } catch (error) {
      console.error('Error performing search:', error);
    }
  };

  return (
    <div>
      <TextField
        label="Search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button variant="contained" color="primary" onClick={handleSearch}>
        Search
      </Button>
      <List>
        {results.map((result, index) => (
          <ListItem key={index}>
            <ListItemText
              primary={result.name || result.term}
              secondary={result.description || result.definition}
            />
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default Search;