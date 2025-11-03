<template>
  <div class="scene-designer">
    <!-- 返回按钮 -->
    <button class="back-button" @click="goBack">← 返回</button>

    <!-- 可滚动内容容器 -->
    <div class="scrollable-content">
      <!-- 标题区 -->
      <div class="header">
        <h1>🌳 生态场景设计</h1>
        <p>在荒漠上种植耐旱树木，见证绿洲的诞生</p>
      </div>

    <!-- 进度信息 -->
    <div class="progress-info">
      <div class="stat-item">
        <span class="stat-label">已种植:</span>
        <span class="stat-value">{{ plantedTrees.length }} 棵树</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">生态指数:</span>
        <span class="stat-value">{{ ecoScore }}%</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">生态等级:</span>
        <span class="stat-value eco-level">{{ ecoLevel }}</span>
      </div>
    </div>

    <!-- 主场景区域 -->
    <div class="scene-container" @click="plantTree" ref="sceneContainer">
      <!-- 内容层 -->
      <div class="scene-content" ref="sceneContent">
        <!-- 背景层 -->
        <div class="scene-background" :class="backgroundClass"></div>
        
        <!-- 装饰元素层 -->
        <div class="decorations">
          <div v-for="bird in birds" :key="bird.id" class="bird" :style="bird.style">🐦</div>
          <div v-for="flower in flowers" :key="flower.id" class="flower" :style="flower.style">🌸</div>
          <div v-for="butterfly in butterflies" :key="butterfly.id" class="butterfly" :style="butterfly.style">🦋</div>
        </div>

        <!-- 树木层 -->
        <div class="trees-layer">
          <div 
            v-for="tree in plantedTrees" 
            :key="tree.id" 
            class="planted-tree"
            :style="{ left: tree.x + 'px', top: tree.y + 'px' }"
            @click.stop="showTreeInfo(tree)"
          >
            <div class="tree-icon" :class="'tree-' + tree.type">{{ tree.icon }}</div>
            <div class="tree-shadow"></div>
          </div>
        </div>

        <!-- 点击提示 -->
        <div v-if="plantedTrees.length === 0" class="click-hint">
          <div class="hint-text">点击荒漠种植你的第一棵树 🌱</div>
        </div>
      </div>
    </div>

    <!-- 树木选择面板 -->
    <div class="tree-selector">
      <h3>选择树种</h3>
      <div class="tree-options">
        <div 
          v-for="treeType in treeTypes" 
          :key="treeType.id"
          class="tree-option"
          :class="{ selected: selectedTreeType === treeType.id }"
          @click="selectTreeType(treeType.id)"
        >
          <div class="tree-icon-large">{{ treeType.icon }}</div>
          <div class="tree-name">{{ treeType.name }}</div>
          <div class="tree-desc">{{ treeType.description }}</div>
        </div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <button @click="clearScene" class="action-btn clear-btn">清空场景</button>
      <button @click="autoPlant" class="action-btn auto-btn" :disabled="autoPlanting">
        {{ autoPlanting ? '种植中...' : '自动种植' }}
      </button>
      <button @click="saveScene" class="action-btn save-btn">保存场景</button>
    </div>

    <!-- 成就提示 -->
    <transition name="achievement">
      <div v-if="showAchievement" class="achievement-popup">
        <div class="achievement-content">
          <div class="achievement-icon">🏆</div>
          <div class="achievement-title">{{ achievementTitle }}</div>
          <div class="achievement-desc">{{ achievementDesc }}</div>
        </div>
      </div>
    </transition>

    <!-- 树木信息弹窗 -->
    <transition name="modal">
      <div v-if="selectedTree" class="tree-modal" @click="selectedTree = null">
        <div class="modal-content" @click.stop>
          <button class="close-btn" @click="selectedTree = null">×</button>
          <div class="modal-tree-icon">{{ selectedTree.icon }}</div>
          <h3>{{ getTreeTypeName(selectedTree.type) }}</h3>
          <p>{{ getTreeTypeDesc(selectedTree.type) }}</p>
          <div class="tree-stats">
            <div class="stat">位置: ({{ Math.round(selectedTree.x) }}, {{ Math.round(selectedTree.y) }})</div>
            <div class="stat">生态贡献: +{{ getTreeEcoValue(selectedTree.type) }}</div>
          </div>
          <button @click="removeTree(selectedTree.id)" class="remove-tree-btn">移除此树</button>
        </div>
      </div>
    </transition>
    </div><!-- 关闭 scrollable-content -->
  </div>
</template>

<script>
export default {
  name: 'SceneDesigner',
  data() {
    return {
      // 树木类型定义
      treeTypes: [
        { 
          id: 'poplar', 
          name: '胡杨', 
          icon: '🌳', 
          description: '沙漠英雄树，耐旱耐盐碱',
          ecoValue: 10
        },
        { 
          id: 'pine', 
          name: '沙地松', 
          icon: '🌲', 
          description: '固沙能手，生命力顽强',
          ecoValue: 8
        },
        { 
          id: 'willow', 
          name: '沙柳', 
          icon: '🌿', 
          description: '防风固沙，快速生长',
          ecoValue: 6
        },
        { 
          id: 'tamarisk', 
          name: '红柳', 
          icon: '🎋', 
          description: '耐旱先锋，改良土壤',
          ecoValue: 7
        },
        { 
          id: 'saxaul', 
          name: '梭梭树', 
          icon: '🌾', 
          description: '荒漠卫士，极耐干旱',
          ecoValue: 9
        },
        { 
          id: 'jujube', 
          name: '沙枣树', 
          icon: '🌴', 
          description: '经济林木，生态经济双赢',
          ecoValue: 8
        },
        { 
          id: 'caragana', 
          name: '柠条', 
          icon: '🌱', 
          description: '优良灌木，固氮改土',
          ecoValue: 7
        }
      ],
      selectedTreeType: 'poplar',
      plantedTrees: [],
      nextTreeId: 1,
      
      // 装饰元素
      birds: [],
      flowers: [],
      butterflies: [],
      
      // 生态指数
      ecoScore: 0,
      
      // 成就系统
      showAchievement: false,
      achievementTitle: '',
      achievementDesc: '',
      achievements: {
        first: false,
        ten: false,
        fifty: false,
        hundred: false,
        oasis: false
      },
      
      // 自动种植
      autoPlanting: false,
      
      // 选中的树木
      selectedTree: null
    }
  },
  computed: {
    backgroundClass() {
      if (this.ecoScore >= 80) return 'bg-paradise'
      if (this.ecoScore >= 60) return 'bg-oasis'
      if (this.ecoScore >= 30) return 'bg-growing'
      if (this.ecoScore >= 10) return 'bg-sprouting'
      return 'bg-desert'
    },
    ecoLevel() {
      if (this.ecoScore >= 80) return '生态天堂 🌈'
      if (this.ecoScore >= 60) return '绿色绿洲 🌳'
      if (this.ecoScore >= 30) return '生机勃发 🌱'
      if (this.ecoScore >= 10) return '初露生机 🌾'
      return '荒漠戈壁 🏜️'
    }
  },
  methods: {
    goBack() {
      this.$router.push('/main')
    },
    
    selectTreeType(typeId) {
      this.selectedTreeType = typeId
    },
    
    plantTree(event) {
      // 获取点击位置
      const rect = this.$refs.sceneContainer.getBoundingClientRect()
      const x = event.clientX - rect.left
      const y = event.clientY - rect.top
      
      // 查找树木类型
      const treeType = this.treeTypes.find(t => t.id === this.selectedTreeType)
      
      // 创建新树木
      const newTree = {
        id: this.nextTreeId++,
        type: this.selectedTreeType,
        icon: treeType.icon,
        x: x - 20, // 居中偏移
        y: y - 30,
        ecoValue: treeType.ecoValue
      }
      
      this.plantedTrees.push(newTree)
      this.updateEcoScore()
      this.checkAchievements()
      this.updateDecorations()
      
      // 播放种植动画效果
      this.playPlantAnimation(x, y)
    },
    
    playPlantAnimation(x, y) {
      // 这里可以添加更复杂的动画效果
      console.log('Planted at:', x, y)
    },
    
    updateEcoScore() {
      const totalValue = this.plantedTrees.reduce((sum, tree) => sum + tree.ecoValue, 0)
      this.ecoScore = Math.min(100, totalValue)
    },
    
    updateDecorations() {
      // 根据生态指数添加装饰元素
      const treeCount = this.plantedTrees.length
      
      // 添加鸟类
      if (treeCount >= 5 && this.birds.length < Math.floor(treeCount / 5)) {
        this.addBird()
      }
      
      // 添加花朵
      if (treeCount >= 10 && this.flowers.length < Math.floor(treeCount / 3)) {
        this.addFlower()
      }
      
      // 添加蝴蝶
      if (treeCount >= 15 && this.butterflies.length < Math.floor(treeCount / 5)) {
        this.addButterfly()
      }
    },
    
    addBird() {
      const bird = {
        id: 'bird-' + Date.now(),
        style: {
          left: Math.random() * 80 + 10 + '%',
          top: Math.random() * 30 + 10 + '%',
          animationDelay: Math.random() * 2 + 's'
        }
      }
      this.birds.push(bird)
    },
    
    addFlower() {
      const flower = {
        id: 'flower-' + Date.now(),
        style: {
          left: Math.random() * 90 + 5 + '%',
          bottom: Math.random() * 20 + 5 + '%'
        }
      }
      this.flowers.push(flower)
    },
    
    addButterfly() {
      const butterfly = {
        id: 'butterfly-' + Date.now(),
        style: {
          left: Math.random() * 80 + 10 + '%',
          top: Math.random() * 60 + 20 + '%',
          animationDelay: Math.random() * 3 + 's'
        }
      }
      this.butterflies.push(butterfly)
    },
    
    checkAchievements() {
      const count = this.plantedTrees.length
      
      if (count === 1 && !this.achievements.first) {
        this.achievements.first = true
        this.showAchievementPopup('播种希望', '你种下了第一棵树！')
      } else if (count === 10 && !this.achievements.ten) {
        this.achievements.ten = true
        this.showAchievementPopup('绿化先锋', '已种植10棵树木！')
      } else if (count === 50 && !this.achievements.fifty) {
        this.achievements.fifty = true
        this.showAchievementPopup('造林能手', '已种植50棵树木！')
      } else if (count === 100 && !this.achievements.hundred) {
        this.achievements.hundred = true
        this.showAchievementPopup('绿化功臣', '已种植100棵树木！')
      }
      
      if (this.ecoScore >= 60 && !this.achievements.oasis) {
        this.achievements.oasis = true
        this.showAchievementPopup('绿洲奇迹', '你创造了一片绿洲！')
      }
    },
    
    showAchievementPopup(title, desc) {
      this.achievementTitle = title
      this.achievementDesc = desc
      this.showAchievement = true
      setTimeout(() => {
        this.showAchievement = false
      }, 3000)
    },
    
    clearScene() {
      if (confirm('确定要清空场景吗？所有树木将被移除。')) {
        this.plantedTrees = []
        this.birds = []
        this.flowers = []
        this.butterflies = []
        this.ecoScore = 0
        this.nextTreeId = 1
      }
    },
    
    async autoPlant() {
      if (this.autoPlanting) return
      
      this.autoPlanting = true
      const count = 20 // 自动种植20棵树
      
      for (let i = 0; i < count; i++) {
        const rect = this.$refs.sceneContainer.getBoundingClientRect()
        const x = Math.random() * (rect.width - 100) + 50
        const y = Math.random() * (rect.height - 100) + 50
        
        // 随机选择树种
        const randomType = this.treeTypes[Math.floor(Math.random() * this.treeTypes.length)]
        this.selectedTreeType = randomType.id
        
        // 模拟点击事件
        const mockEvent = {
          clientX: rect.left + x,
          clientY: rect.top + y
        }
        this.plantTree(mockEvent)
        
        // 延迟以产生动画效果
        await new Promise(resolve => setTimeout(resolve, 200))
      }
      
      this.autoPlanting = false
    },
    
    saveScene() {
      const sceneData = {
        trees: this.plantedTrees,
        ecoScore: this.ecoScore,
        achievements: this.achievements,
        timestamp: new Date().toISOString()
      }
      
      localStorage.setItem('greenGoldScene', JSON.stringify(sceneData))
      alert('场景已保存！')
    },
    
    loadScene() {
      const saved = localStorage.getItem('greenGoldScene')
      if (saved) {
        const sceneData = JSON.parse(saved)
        this.plantedTrees = sceneData.trees || []
        this.ecoScore = sceneData.ecoScore || 0
        this.achievements = sceneData.achievements || {}
        this.nextTreeId = Math.max(...this.plantedTrees.map(t => t.id), 0) + 1
        this.updateDecorations()
      }
    },
    
    showTreeInfo(tree) {
      this.selectedTree = tree
    },
    
    getTreeTypeName(typeId) {
      const type = this.treeTypes.find(t => t.id === typeId)
      return type ? type.name : '未知树种'
    },
    
    getTreeTypeDesc(typeId) {
      const type = this.treeTypes.find(t => t.id === typeId)
      return type ? type.description : ''
    },
    
    getTreeEcoValue(typeId) {
      const type = this.treeTypes.find(t => t.id === typeId)
      return type ? type.ecoValue : 0
    },
    
    removeTree(treeId) {
      const index = this.plantedTrees.findIndex(t => t.id === treeId)
      if (index > -1) {
        this.plantedTrees.splice(index, 1)
        this.updateEcoScore()
        this.selectedTree = null
      }
    }
  },
  mounted() {
    this.loadScene()
  }
}
</script>

<style scoped>
.scene-designer {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 1rem;
  padding-bottom: 2rem;
  position: relative;
  overflow: hidden; /* 外层容器隐藏溢出 */
}

/* 可滚动内容容器 */
.scrollable-content {
  max-height: calc(100vh - 2rem); /* 减去外层padding */
  overflow-x: hidden;
  overflow-y: auto;
  padding-right: 0.5rem; /* 为滚动条留空间 */
}

/* 自定义滚动条样式 */
.scrollable-content::-webkit-scrollbar {
  width: 10px;
}

.scrollable-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 5px;
}

.scrollable-content::-webkit-scrollbar-thumb {
  background: #4caf50;
  border-radius: 5px;
}

.scrollable-content::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

.back-button {
  position: fixed;
  top: 1rem;
  left: 1rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #4caf50;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  color: #4caf50;
  font-weight: bold;
  z-index: 100;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: #4caf50;
  color: white;
  transform: translateX(-5px);
}

.header {
  text-align: center;
  margin-bottom: 1rem;
  padding-top: 3.5rem;
}

.header h1 {
  font-size: 2rem;
  color: #2e7d32;
  margin-bottom: 0.5rem;
}

.header p {
  color: #666;
  font-size: 1rem;
}

.progress-info {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-label {
  font-weight: bold;
  color: #555;
}

.stat-value {
  font-size: 1.2rem;
  color: #4caf50;
  font-weight: bold;
}

.eco-level {
  font-size: 1rem;
}

.scene-container {
  position: relative;
  width: 100%;
  max-width: 1200px;
  height: 500px;
  margin: 0 auto 1rem;
  border-radius: 15px;
  overflow: hidden;
  cursor: crosshair;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  transition: all 0.5s ease;
}

/* 内容层 */
.scene-content {
  position: relative;
  width: 100%;
  height: 100%;
}

.scene-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition: all 1s ease;
}

.bg-desert {
  background: linear-gradient(180deg, #ffd89b 0%, #deb887 100%);
}

.bg-sprouting {
  background: linear-gradient(180deg, #ffd89b 0%, #d4c4a0 50%, #c4d4a0 100%);
}

.bg-growing {
  background: linear-gradient(180deg, #a8e6cf 0%, #dcedc1 50%, #b4d4a0 100%);
}

.bg-oasis {
  background: linear-gradient(180deg, #87ceeb 0%, #a8e6cf 50%, #66bb6a 100%);
}

.bg-paradise {
  background: linear-gradient(180deg, #87ceeb 0%, #98d8c8 30%, #6bcf7f 60%, #43a047 100%);
}

.decorations {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.bird {
  position: absolute;
  font-size: 1.5rem;
  animation: fly 10s ease-in-out infinite;
}

@keyframes fly {
  0%, 100% { transform: translateX(0) translateY(0); }
  25% { transform: translateX(100px) translateY(-20px); }
  50% { transform: translateX(200px) translateY(0); }
  75% { transform: translateX(100px) translateY(20px); }
}

.flower {
  position: absolute;
  font-size: 1.2rem;
  animation: bloom 2s ease-in-out;
}

@keyframes bloom {
  0% { transform: scale(0); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.butterfly {
  position: absolute;
  font-size: 1.3rem;
  animation: flutter 6s ease-in-out infinite;
}

@keyframes flutter {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-15px) rotate(10deg); }
  50% { transform: translateY(0) rotate(0deg); }
  75% { transform: translateY(-15px) rotate(-10deg); }
}

.trees-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.planted-tree {
  position: absolute;
  cursor: pointer;
  transition: transform 0.2s ease;
  animation: treeGrow 0.5s ease-out;
}

@keyframes treeGrow {
  0% { transform: scale(0) translateY(20px); opacity: 0; }
  60% { transform: scale(1.1) translateY(0); }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}

.planted-tree:hover {
  transform: scale(1.2);
  filter: drop-shadow(0 0 10px rgba(76, 175, 80, 0.6));
}

.tree-icon {
  font-size: 2.5rem;
  text-align: center;
}

.tree-shadow {
  width: 30px;
  height: 10px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  margin: 0 auto;
  filter: blur(3px);
}

.click-hint {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  pointer-events: none;
}

.hint-text {
  font-size: 1.5rem;
  color: #666;
  background: rgba(255, 255, 255, 0.8);
  padding: 1rem 2rem;
  border-radius: 25px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 1; transform: translate(-50%, -50%) scale(1.05); }
}

.tree-selector {
  max-width: 1200px;
  margin: 0 auto 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.tree-selector h3 {
  text-align: center;
  color: #2e7d32;
  margin-bottom: 1rem;
}

.tree-options {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 0.5rem;
  scroll-behavior: smooth;
}

/* 自定义滚动条样式 */
.tree-options::-webkit-scrollbar {
  height: 8px;
}

.tree-options::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.tree-options::-webkit-scrollbar-thumb {
  background: #4caf50;
  border-radius: 10px;
}

.tree-options::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

.tree-option {
  flex: 0 0 150px;
  min-width: 150px;
  padding: 1rem;
  background: white;
  border: 3px solid transparent;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s ease;
}

.tree-option:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.tree-option.selected {
  border-color: #4caf50;
  background: #e8f5e9;
}

.tree-icon-large {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.tree-name {
  font-weight: bold;
  color: #333;
  margin-bottom: 0.25rem;
}

.tree-desc {
  font-size: 0.85rem;
  color: #666;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-btn {
  background: #f44336;
  color: white;
}

.clear-btn:hover {
  background: #d32f2f;
  transform: scale(1.05);
}

.auto-btn {
  background: #2196f3;
  color: white;
}

.auto-btn:hover:not(:disabled) {
  background: #1976d2;
  transform: scale(1.05);
}

.auto-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.save-btn {
  background: #4caf50;
  color: white;
}

.save-btn:hover {
  background: #388e3c;
  transform: scale(1.05);
}

/* 成就弹窗 */
.achievement-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  text-align: center;
  min-width: 300px;
}

.achievement-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.achievement-icon {
  font-size: 4rem;
  animation: bounce 0.6s ease;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.achievement-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.achievement-desc {
  font-size: 1rem;
  opacity: 0.9;
}

.achievement-enter-active, .achievement-leave-active {
  transition: all 0.5s ease;
}

.achievement-enter-from, .achievement-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.5);
}

/* 树木信息弹窗 */
.tree-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  max-width: 400px;
  width: 90%;
  position: relative;
  text-align: center;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

.modal-tree-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.modal-content h3 {
  color: #2e7d32;
  margin-bottom: 0.5rem;
}

.modal-content p {
  color: #666;
  margin-bottom: 1rem;
}

.tree-stats {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.stat {
  margin: 0.5rem 0;
  color: #555;
}

.remove-tree-btn {
  padding: 0.5rem 1.5rem;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
}

.remove-tree-btn:hover {
  background: #d32f2f;
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .scrollable-content {
    max-height: calc(100vh - 1rem); /* 移动端更紧凑的间距 */
  }

  .header h1 {
    font-size: 1.5rem;
  }

  .progress-info {
    flex-direction: column;
    gap: 0.5rem;
  }

  .scene-container {
    height: 400px;
  }

  .tree-options {
    gap: 0.75rem;
  }

  .tree-option {
    flex: 0 0 130px;
    min-width: 130px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}
</style>
