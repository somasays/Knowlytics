<template>
  <div class="dashboard">
    <div class="tabs">
      <a href="#" class="active">All</a>
      <a href="#">@Mentions <span class="counter">0</span></a>
      <a href="#">Tasks <span class="counter">0</span></a>
    </div>
    <div class="content">
      <div class="no-data-message">
        <i class="fas fa-list"></i>
        <p>
          Right now, there are no updates in the data assets you own or follow. 
          <a href="#">Haven't explored yet?</a> Dive in and claim ownership or follow the data assets 
          that interest you to stay informed about their latest activities!
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
}
</script>

<style scoped lang="scss">
.dashboard {
  padding: 20px;

  .tabs {
    margin-bottom: 20px;
    border-bottom: 1px solid #dee2e6;

    a {
      display: inline-block;
      padding: 10px 15px;
      color: #495057;
      text-decoration: none;
      margin-right: 10px;

      &.active {
        color: #007bff;
        border-bottom: 2px solid #007bff;
      }

      .counter {
        background-color: #6c757d;
        color: white;
        border-radius: 10px;
        padding: 2px 6px;
        font-size: 0.8em;
        margin-left: 5px;
      }
    }
  }

  .content {
    .no-data-message {
      text-align: center;
      padding: 40px 20px;
      background-color: white;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

      i {
        font-size: 48px;
        color: #6c757d;
        margin-bottom: 20px;
      }

      p {
        color: #495057;
        max-width: 600px;
        margin: 0 auto;

        a {
          color: #007bff;
          text-decoration: none;

          &:hover {
            text-decoration: underline;
          }
        }
      }
    }
  }
}
</style>