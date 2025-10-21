<template>
  <div class="main-page">
    <div class="explore-container">
      <div class="explore-item" @click="goToSection('anji')">
        <div class="icon">🌳</div>
        <h2>安吉变迁</h2>
        <p>探索安吉从矿山小县到绿水青山的蝶变之路</p>
        <div class="arrow-animation"></div>
      </div>

      <div class="explore-item" @click="goToSection('knowledge')">
        <div class="icon">📚</div>
        <h2>相关知识</h2>
        <p>了解"两山理论"的深刻内涵与实践</p>
        <div class="arrow-animation"></div>
      </div>

      <div class="explore-item" @click="goToSection('quiz')">
        <div class="icon">✍️</div>
        <h2>智能答题</h2>
        <p>测试你对绿色发展理念的理解</p>
        <div class="arrow-animation"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    goToSection(section) {
      if (section === 'anji') {
        this.$router.push('/anji-timeline')
      } else if (section === 'quiz') {
        this.$router.push('/quiz')
      } else {
        // 后续添加其他导航逻辑
        console.log('Navigate to:', section)
      }
    }
  }
}
</script>

<style scoped>
.main-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #ffffff 0%, #e8f4e9 100%);
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

/* 添加装饰性背景元素 */
.main-page::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(76, 175, 80, 0.05) 0%, transparent 60%);
  animation: rotate 60s linear infinite;
  z-index: 0;
}

.map-container {
  flex: 1;
  position: relative;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.location {
  position: absolute;
  cursor: pointer;
  transition: all 0.3s ease;
}

.anji-location {
  top: 30%;
  left: 20%;
}

.knowledge-location {
  top: 30%;
  right: 20%;
}

.quiz-location {
  bottom: 30%;
  right: 20%;
}

.location-marker {
  position: relative;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.marker-icon {
  font-size: 1.8rem;
  z-index: 2;
}

.pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(210, 63, 87, 0.4);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.location-info {
  position: absolute;
  top: 120%;
  left: 50%;
  transform: translateX(-50%) scale(0.9);
  background: rgba(255, 255, 255, 0.95);
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  width: 200px;
  opacity: 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.location:hover .location-info {
  opacity: 1;
  transform: translateX(-50%) scale(1);
}

.location h2 {
  color: #d23f57;
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.location p {
  color: #bf4f65;
  font-size: 0.9rem;
  line-height: 1.4;
}

.path-lines {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
}

.path-line {
  fill: none;
  stroke: rgba(210, 63, 87, 0.3);
  stroke-width: 2;
  stroke-dasharray: 8;
  animation: dash 30s linear infinite;
}



@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.6;
  }
  70% {
    transform: scale(1.5);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 0;
  }
}

@keyframes dash {
  to {
    stroke-dashoffset: 1000;
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 响应式调整 */
@media screen and (max-width: 768px) {
  .location {
    position: relative;
    top: auto !important;
    left: auto !important;
    right: auto !important;
    bottom: auto !important;
    margin: 2rem 0;
  }

  .map-container {
    flex-direction: column;
    padding: 1rem;
  }

  .location-info {
    position: relative;
    top: 1rem;
    opacity: 1;
    transform: translateX(-50%) scale(1);
  }

  .path-lines {
    display: none;
  }

  .compass {
    top: 1rem;
    left: 1rem;
    width: 40px;
    height: 40px;
  }

  .compass-inner {
    width: 30px;
    height: 30px;
  }

  .nav-item {
    padding: 0.6rem 1rem;
  }

  .nav-text {
    font-size: 0.9rem;
  }
}

.explore-container {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  max-width: 900px;
  margin: 0 auto;
  padding: 3rem 2rem;
  flex: 1;
  position: relative;
  z-index: 1;
  perspective: 1000px;
}

.explore-item {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 2.5% 5%;
  cursor: pointer;
  position: relative;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
  text-align: center;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
  transform-style: preserve-3d;
}

.explore-item:hover {
  transform: translateY(-8px) rotateX(2deg) rotateY(-2deg);
  border-color: #4CAF50;
  box-shadow: 
    0 20px 40px rgba(76, 175, 80, 0.15),
    0 0 20px rgba(76, 175, 80, 0.1);
}

.explore-item .icon {
  font-size: 1rem;
  margin-bottom: 1.5rem;
  transform-style: preserve-3d;
  transform: translateZ(20px);
  transition: all 0.5s ease;
}

.explore-item:hover .icon {
  transform: translateZ(30px) scale(1.1);
}

.explore-item h2 {
  color: #1b4d2e;
  font-size: 2rem;
  margin-bottom: 1.2rem;
  font-weight: 700;
  transform: translateZ(15px);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.5px;
}

.explore-item p {
  color: #4a6b57;
  font-size: 1.2rem;
  line-height: 1.6;
  transform: translateZ(10px);
  max-width: 80%;
  margin: 0 auto;
}

.arrow-animation {
  position: absolute;
  right: 3%;
  top: 50%;
  width: 20px;
  height: 20px;
  border-right: 3px solid #4CAF50;
  border-bottom: 3px solid #4CAF50;
  transform: translateY(-50%) rotate(-45deg);
  opacity: 0;
  transition: all 0.3s ease;
}

.explore-item:hover .arrow-animation {
  opacity: 1;
  right: 2%;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}
</style>