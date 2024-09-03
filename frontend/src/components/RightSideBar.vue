<template>
  <div class="right-sidebar">
    <div class="announcements">
      <h3>Recent Announcements</h3>
      <p v-if="!announcements.length">
        <i class="fas fa-bullhorn"></i>
        No announcement data available.
      </p>
      <ul v-else>
        <li v-for="announcement in announcements" :key="announcement.id">
          {{ announcement.content }}
        </li>
      </ul>
    </div>
    <div class="following">
      <h3>Following</h3>
      <p v-if="!following.length">
        <i class="far fa-star"></i>
        Start Exploring! and Follow the Data Assets that interests you.
        <a href="#">Learn More</a>
      </p>
      <ul v-else>
        <li v-for="item in following" :key="item.id">
          {{ item.name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RightSideBar',
  data() {
    return {
      announcements: [],
      following: []
    }
  }
}
</script>

<style scoped lang="scss">
.right-sidebar {
  width: 250px;
  padding: 20px;
  background-color: white;
  border-left: 1px solid #e0e0e0;
  overflow-y: auto;
  flex-shrink: 0;

  h3 {
    margin-bottom: 10px;
    color: #343a40;
  }

  .announcements, .following {
    margin-bottom: 20px;
  }

  p, ul {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  a {
    color: #007bff;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }

  i {
    margin-right: 5px;
  }
}
</style>