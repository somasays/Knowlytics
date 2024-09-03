<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div class="dashboard-content">
      <div class="main-content">
        <div class="dashboard-card">
          <h2>Recent Activity</h2>
          <ul>
            <li>Updated Asset: Customer Data</li>
            <li>New Comment on: Sales Report</li>
            <li>Created Asset: Marketing Campaign</li>
          </ul>
        </div>
        <div class="dashboard-card">
          <h2>Quick Actions</h2>
          <button>Create New Asset</button>
          <button>Generate Report</button>
          <button>Invite Team Member</button>
        </div>
      </div>
      <div class="right-sidebar">
        <div class="sidebar-section">
          <h3>Recent Announcements</h3>
          <p>No announcement data available.</p>
        </div>
        <div class="sidebar-section">
          <h3>Following</h3>
          <p>
            Start Exploring! and Follow the Data Assets that interests you.
            <a href="#">Learn More</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardView'
}
</script>

<style scoped lang="scss">
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px;

  h1 {
    margin-bottom: 20px;
    color: #2c3e50;
  }

  .dashboard-content {
    display: flex;
    flex-grow: 1;
    gap: 20px;
  }

  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .dashboard-card {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    h2 {
      margin-bottom: 15px;
      color: #34495e;
    }

    ul {
      list-style-type: none;
      padding: 0;

      li {
        margin-bottom: 10px;
        padding: 10px;
        background-color: #f5f7fa;
        border-radius: 4px;
      }
    }

    button {
      display: block;
      width: 100%;
      padding: 10px;
      margin-bottom: 10px;
      background-color: #3498db;
      color: #ffffff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.3s;

      &:hover {
        background-color: #2980b9;
      }
    }
  }

  .right-sidebar {
    width: 250px;
    flex-shrink: 0;

    .sidebar-section {
      background-color: #ffffff;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      margin-bottom: 20px;

      h3 {
        margin-bottom: 10px;
        color: #34495e;
      }

      p {
        color: #5c6a7a;
      }

      a {
        color: #3498db;
        text-decoration: none;

        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
}
</style>