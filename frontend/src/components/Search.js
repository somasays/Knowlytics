import React, { useState } from 'react';
import { Paper, Typography, Box, Tabs, Tab, List, ListItem, ListItemText, Divider } from '@mui/material';
import AnnouncementIcon from '@mui/icons-material/Announcement';

const Search = () => {
  const [tabValue, setTabValue] = useState(0);

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
          <Typography variant="body1" color="text.secondary">
            Right now, there are no updates in the data assets you own or follow. Haven't explored yet? Dive in and claim ownership or follow the data assets
          </Typography>
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

export default Search;