<template>
  <div class="start-page">
    <button class="explore-btn" @click="startExplore">开始探索</button>
  </div>
</template>

<script>
export default {
  name: 'StartPage',
  methods: {
    startExplore() {
      this.$router.push('/main')
    }
  }
}
</script>

<style scoped>
.start-page {
  width: 100vw;
  height: 100vh;
  background-image: url('../assets/images/1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  padding: 0;
  position: fixed;
  top: 0;
  left: 0;
  overflow: hidden;
  margin: 0;
}

.explore-btn {
  padding: 12px 30px;
  font-size: 1.1rem;
  background-color: rgba(255, 255, 255, 0.9);
  color: #333;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 5vh;
  z-index: 1;
}

@media screen and (min-width: 768px) {
  .start-page {
    background-size: contain;
  }
  .explore-btn {
    padding: 15px 40px;
    font-size: 1.2rem;
    border-radius: 30px;
  }
}

@media screen and (max-width: 767px) {
  .start-page {
    background-size: cover;
    background-position: center center;
  }
  .explore-btn {
    margin-bottom: 30px;
    padding: 10px 25px;
    font-size: 1rem;
  }
}

.explore-btn:hover {
  background-color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>