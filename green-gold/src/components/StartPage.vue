<template>
  <div class="start-page">
    <button class="explore-btn" @click="startExplore">
      <span class="btn-text">开始探索</span>
    </button>
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
  width: 200px;
  height: 200px;
  background-image: url('../assets/start.webp');
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  background-color: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 5vh;
  z-index: 1;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.btn-text {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
  text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8),
               -1px -1px 2px rgba(255, 255, 255, 0.6);
  letter-spacing: 2px;
  transition: all 0.3s ease;
  z-index: 2;
}

@media screen and (min-width: 768px) {
  .start-page {
    background-size: contain;
  }
  .explore-btn {
    width: 250px;
    height: 250px;
  }
  .btn-text {
    font-size: 1.4rem;
  }
}

@media screen and (max-width: 767px) {
  .start-page {
    background-size: cover;
    background-position: center center;
  }
  .explore-btn {
    margin-bottom: 30px;
    width: 150px;
    height: 150px;
  }
  .btn-text {
    font-size: 1rem;
  }
}

.explore-btn:hover {
  transform: scale(1.1) translateY(-5px);
  filter: brightness(1.1) drop-shadow(0 8px 16px rgba(0, 0, 0, 0.3));
}

.explore-btn:hover .btn-text {
  transform: scale(1.05);
  text-shadow: 2px 2px 6px rgba(255, 255, 255, 1),
               -1px -1px 3px rgba(255, 255, 255, 0.8);
}

.explore-btn:active {
  transform: scale(1.05) translateY(-2px);
  filter: brightness(1.05);
}
</style>