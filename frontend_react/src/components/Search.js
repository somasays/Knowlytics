import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, Tabs, Tab, List, ListItem, ListItemText } from '@mui/material';
import AnnouncementIcon from '@mui/icons-material/Announcement';

const Search = ({ onSearchResults }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [noResults, setNoResults] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [tabValue, setTabValue] = useState(0);

  console.log("Search component rendered. State:", { query, results, noResults, hasSearched });

  useEffect(() => {
    if (onSearchResults) {
      onSearchResults((searchQuery, searchResults) => {
        console.log("handleSearchResults called with:", { searchQuery, searchResults });
        
        setQuery(searchQuery || '');
        setResults(searchResults || []);
        setNoResults((searchResults || []).length === 0);
        setHasSearched(true);
        
        console.log("State updated in handleSearchResults");
      });
    }
  }, [onSearchResults]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <Box sx={{ flexGrow: 1, mr: 2 }}>
        <Paper elevation={0} sx={{ p: 2, mb: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="basic tabs example">
            <Tab label="All" />
            <Tab label="@Mentions" />
            <Tab label="Tasks" />
          </Tabs>
        </Paper>
        <Paper elevation={0} sx={{ p: 2, textAlign: 'center' }}>
          {hasSearched ? (
            query ? (
              noResults ? (
                <Typography variant="body1" color="text.secondary">
                  No results found for "{query}". Please try a different search term or check your spelling.
                </Typography>
              ) : (
                results.length > 0 ? (
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
                ) : (
                  <Typography variant="body1" color="text.secondary">
                    Loading results...
                  </Typography>
                )
              )
            ) : (
              <Typography variant="body1" color="text.secondary">
                Please enter a search query.
              </Typography>
            )
          ) : (
            <Typography variant="body1" color="text.secondary">
              Enter a search query to find data assets
            </Typography>
          )}
        </Paper>
      </Box>
      <Box sx={{ width: 300 }}>
        <Paper elevation={0} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Recent Announcements
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 100 }}>
            <AnnouncementIcon sx={{ fontSize: 40, color: 'text.secondary', mr: 1 }} />
            <Typography variant="body2" color="text.secondary">
              No announcement data available.
            </Typography>
          </Box>
        </Paper>
        <Paper elevation={0} sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Following
          </Typography>
          <List>
            {/* Add list items for followed data assets here */}
          </List>
        </Paper>
      </Box>
    </Box>
  );
};

export default React.memo(Search);