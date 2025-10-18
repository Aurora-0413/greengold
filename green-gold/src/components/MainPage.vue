<template>
  <div class="main-page">
    <div class="content">
      <!-- 主要内容区域 -->
    </div>
    <nav class="navigation">
      <div class="nav-item" @click="goToSection('anji')">安吉变迁</div>
      <div class="nav-item" @click="goToSection('knowledge')">相关知识</div>
      <div class="nav-item" @click="goToSection('quiz')">智能答题</div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    goToSection(section) {
      // 后续添加导航逻辑
      console.log('Navigate to:', section)
    }
  }
}
</script>

&lt;style scoped>
.main-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  /* 暂时留空 */
}

.navigation {
  height: 60px;
  background-color: #4CAF50;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.nav-item {
  color: white;
  cursor: pointer;
  padding: 1rem 2rem;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background-color: #45a049;
}
&lt;/style>