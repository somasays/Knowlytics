import Search from './Search';
import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, Container, CssBaseline, Box, IconButton, InputBase, Paper, Snackbar, Alert } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import NotificationsIcon from '@mui/icons-material/Notifications';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import axios from 'axios';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

const Layout = ({ children }) => {
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleSearch = async (event) => {
    event.preventDefault();
    console.log("handleSearch called. Current query:", query);
    
    if (query.trim()) {
      try {
        console.log("Performing search for query:", query);
        const response = await axios.get(`http://localhost:8000/api/v1/search?query=${query}`);
        const searchResults = response.data.results;
        console.log("Search results received:", searchResults);
        
        // Update Search component
        const searchComponent = React.Children.only(children);
        if (React.isValidElement(searchComponent) && searchComponent.props.onSearchResults) {
          searchComponent.props.onSearchResults(query, searchResults);
        }
      } catch (error) {
        console.error('Error performing search:', error);
        setError('An error occurred while searching. Please try again later.');
        setOpenSnackbar(true);
        
        // Update Search component with error
        const searchComponent = React.Children.only(children);
        if (React.isValidElement(searchComponent) && searchComponent.props.onSearchResults) {
          searchComponent.props.onSearchResults(query, []);
        }
      }
    } else {
      console.log("Search not performed: empty query");
    }
  };

  const handleCloseSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSnackbar(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <AppBar position="static" color="default" elevation={0}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Knowlytics
            </Typography>
            <Paper
              component="form"
              onSubmit={handleSearch}
              sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: 400 }}
            >
              <InputBase
                sx={{ ml: 1, flex: 1 }}
                placeholder="Search for Data Assets"
                inputProps={{ 'aria-label': 'search for data assets' }}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <IconButton type="submit" sx={{ p: '10px' }} aria-label="search">
                <SearchIcon />
              </IconButton>
            </Paper>
            <IconButton color="inherit">
              <NotificationsIcon />
            </IconButton>
            <IconButton color="inherit">
              <HelpOutlineIcon />
            </IconButton>
            <IconButton color="inherit">
              <AccountCircleIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
        <Container component="main" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
          {children}
        </Container>
      </Box>
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </ThemeProvider>
  );
};

export default Layout;