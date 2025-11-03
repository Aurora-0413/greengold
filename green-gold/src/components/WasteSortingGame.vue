<template>
  <div class="waste-sorting-wrapper">
    <div class="waste-sorting-game">
      <div class="header">
        <h2>🎮 垃圾分类挑战</h2>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
          <span class="progress-text">{{ currentIndex + 1 }} / {{ items.length }}</span>
        </div>
      </div>
    
    <div v-if="!gameOver" class="game-content">
      <div class="item-card" :class="{ 'shake': feedback && !feedback.correct }">
        <div class="waste-img-container">
          <div class="waste-img">{{ currentItem.img }}</div>
        </div>
        <p class="item-name">{{ currentItem.name }}</p>
        <p class="item-hint">👇 请选择正确的垃圾桶</p>
      </div>
      
      <div class="bins-container">
        <button 
          v-for="bin in bins" 
          :key="bin.type" 
          @click="chooseBin(bin.type)" 
          class="bin-btn"
          :class="{ 
            'selected': feedback && bin.type === currentItem.type,
            'wrong': feedback && !feedback.correct && bin.type !== currentItem.type,
            'disabled': feedback
          }"
          :disabled="feedback !== null"
        >
          <div class="bin-icon">{{ bin.img }}</div>
          <span class="bin-label">{{ bin.label }}</span>
        </button>
      </div>
      
      <transition name="feedback-slide">
        <div v-if="feedback" class="feedback-card" :class="{ correct: feedback.correct, wrong: !feedback.correct }">
          <div class="feedback-icon">{{ feedback.correct ? '🎉' : '😅' }}</div>
          <p class="feedback-message">{{ feedback.message }}</p>
          <p v-if="feedback.knowledge" class="knowledge-text">
            <span class="knowledge-icon">💡</span>
            {{ feedback.knowledge }}
          </p>
          <button @click="nextItem" class="next-btn">
            {{ currentIndex < items.length - 1 ? '下一题 →' : '查看结果 🎯' }}
          </button>
        </div>
      </transition>
      
      <div class="score-badge">
        <span class="score-label">得分</span>
        <span class="score-value">{{ score }}</span>
      </div>
    </div>
    
    <transition name="result-fade">
      <div v-if="gameOver" class="result-area">
        <div class="result-icon">{{ getResultIcon() }}</div>
        <h3 class="result-title">游戏结束！</h3>
        <div class="final-score">
          <span class="score-text">总得分</span>
          <span class="score-number">{{ score }}</span>
          <span class="score-total">/ {{ items.length }}</span>
        </div>
        <p class="result-message">{{ getResultMessage() }}</p>
        <button @click="restartGame" class="restart-btn">
          🔄 再玩一次
        </button>
      </div>
    </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WasteSortingGame',
  data() {
    return {
      // 全部物品库（约50个）
      allItems: [
        { name: '塑料瓶', type: 'recyclable', img: '🧴', knowledge: '塑料瓶属于可回收物，应投入蓝色垃圾桶。' },
        { name: '玻璃瓶', type: 'recyclable', img: '�', knowledge: '玻璃瓶属于可回收物，应投入蓝色垃圾桶。' },
        { name: '易拉罐', type: 'recyclable', img: '🥫', knowledge: '易拉罐属于可回收物，应投入蓝色垃圾桶。' },
        { name: '旧报纸', type: 'recyclable', img: '📰', knowledge: '旧报纸属于可回收物，应投入蓝色垃圾桶。' },
        { name: '纸箱', type: 'recyclable', img: '�', knowledge: '纸箱属于可回收物，应投入蓝色垃圾桶。' },
        { name: '金属罐', type: 'recyclable', img: '🏺', knowledge: '金属罐属于可回收物，应投入蓝色垃圾桶。' },
        { name: '旧书本', type: 'recyclable', img: '📚', knowledge: '旧书本属于可回收物，应投入蓝色垃圾桶。' },
        { name: '饮料盒', type: 'recyclable', img: '�', knowledge: '饮料盒属于可回收物，应投入蓝色垃圾桶。' },
        { name: '旧衣服', type: 'recyclable', img: '👕', knowledge: '旧衣服属于可回收物，应投入蓝色垃圾桶。' },
        { name: '塑料袋', type: 'recyclable', img: '🛍️', knowledge: '塑料袋属于可回收物，应投入蓝色垃圾桶。' },
        { name: '香蕉皮', type: 'kitchen', img: '🍌', knowledge: '香蕉皮属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '剩饭剩菜', type: 'kitchen', img: '🍚', knowledge: '剩饭剩菜属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '苹果核', type: 'kitchen', img: '🍏', knowledge: '苹果核属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '西瓜皮', type: 'kitchen', img: '🍉', knowledge: '西瓜皮属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '鸡蛋壳', type: 'kitchen', img: '🥚', knowledge: '鸡蛋壳属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '菜叶', type: 'kitchen', img: '🥬', knowledge: '菜叶属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '骨头', type: 'kitchen', img: '🍖', knowledge: '骨头属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '茶叶渣', type: 'kitchen', img: '🍵', knowledge: '茶叶渣属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '咖啡渣', type: 'kitchen', img: '☕', knowledge: '咖啡渣属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '果皮', type: 'kitchen', img: '🍊', knowledge: '果皮属于厨余垃圾，应投入绿色垃圾桶。' },
        { name: '废电池', type: 'hazardous', img: '🔋', knowledge: '废电池属于有害垃圾，应投入红色垃圾桶。' },
        { name: '过期药品', type: 'hazardous', img: '💊', knowledge: '过期药品属于有害垃圾，应投入红色垃圾桶。' },
        { name: '废灯泡', type: 'hazardous', img: '💡', knowledge: '废灯泡属于有害垃圾，应投入红色垃圾桶。' },
        { name: '废温度计', type: 'hazardous', img: '🌡️', knowledge: '废温度计属于有害垃圾，应投入红色垃圾桶。' },
        { name: '杀虫剂瓶', type: 'hazardous', img: '🧴', knowledge: '杀虫剂瓶属于有害垃圾，应投入红色垃圾桶。' },
        { name: '油漆桶', type: 'hazardous', img: '🪣', knowledge: '油漆桶属于有害垃圾，应投入红色垃圾桶。' },
        { name: '废胶片', type: 'hazardous', img: '🎞️', knowledge: '废胶片属于有害垃圾，应投入红色垃圾桶。' },
        { name: '废化妆品', type: 'hazardous', img: '💄', knowledge: '废化妆品属于有害垃圾，应投入红色垃圾桶。' },
        { name: '废农药', type: 'hazardous', img: '🧪', knowledge: '废农药属于有害垃圾，应投入红色垃圾桶。' },
        { name: '废水银', type: 'hazardous', img: '⚗️', knowledge: '废水银属于有害垃圾，应投入红色垃圾桶。' },
        { name: '纸巾', type: 'other', img: '🧻', knowledge: '纸巾属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '陶瓷碎片', type: 'other', img: '🏺', knowledge: '陶瓷碎片属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '一次性餐具', type: 'other', img: '🍽️', knowledge: '一次性餐具属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '烟头', type: 'other', img: '🚬', knowledge: '烟头属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '尿不湿', type: 'other', img: '🍼', knowledge: '尿不湿属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '破碎花盆', type: 'other', img: '🪴', knowledge: '破碎花盆属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '灰尘', type: 'other', img: '🌫️', knowledge: '灰尘属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '塑料餐盒', type: 'other', img: '🍱', knowledge: '塑料餐盒属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '泡沫塑料', type: 'other', img: '🧊', knowledge: '泡沫塑料属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '碎玻璃', type: 'other', img: '🔪', knowledge: '碎玻璃属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '牙签', type: 'other', img: '🦷', knowledge: '牙签属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '棉签', type: 'other', img: '🪥', knowledge: '棉签属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '头发', type: 'other', img: '💇', knowledge: '头发属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '口罩', type: 'other', img: '😷', knowledge: '口罩属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '指甲', type: 'other', img: '💅', knowledge: '指甲属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '宠物粪便', type: 'other', img: '💩', knowledge: '宠物粪便属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '碎瓷砖', type: 'other', img: '🧱', knowledge: '碎瓷砖属于其他垃圾，应投入灰色垃圾桶。' },
        { name: '胶带', type: 'other', img: '📎', knowledge: '胶带属于其他垃圾，应投入灰色垃圾桶。' }
      ],
      items: [], // 本轮题目
      bins: [
        { type: 'recyclable', label: '可回收物', img: '♻️' }, // 可回收
        { type: 'kitchen', label: '厨余垃圾', img: '🍃' },   // 厨余
        { type: 'hazardous', label: '有害垃圾', img: '☢️' }, // 有害
        { type: 'other', label: '其他垃圾', img: '🗑️' }     // 其他
      ],
      currentIndex: 0,
      score: 0,
      feedback: null,
      gameOver: false
    };
  },
  created() {
    this.startNewGame();
  },
  computed: {
    currentItem() {
      return this.items[this.currentIndex];
    },
    progressPercent() {
      return ((this.currentIndex + 1) / this.items.length) * 100;
    }
  },
  methods: {
    chooseBin(type) {
      if (this.feedback) return;
      if (type === this.currentItem.type) {
        this.score++;
        this.feedback = {
          correct: true,
          message: '分类正确！',
          knowledge: this.currentItem.knowledge
        };
      } else {
        this.feedback = {
          correct: false,
          message: '分类错误！',
          knowledge: this.currentItem.knowledge
        };
      }
    },
    nextItem() {
      if (this.currentIndex < this.items.length - 1) {
        this.currentIndex++;
        this.feedback = null;
      } else {
        this.gameOver = true;
      }
    },
    restartGame() {
      this.startNewGame();
    },
    startNewGame() {
      // 随机抽取5个题目
      this.items = this.shuffle(this.allItems).slice(0, 5);
      this.currentIndex = 0;
      this.score = 0;
      this.feedback = null;
      this.gameOver = false;
    },
    shuffle(arr) {
      // 洗牌算法
      let array = arr.slice();
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    },
    getResultIcon() {
      const percent = (this.score / this.items.length) * 100;
      if (percent === 100) return '🏆';
      if (percent >= 80) return '🌟';
      if (percent >= 60) return '👍';
      if (percent >= 40) return '💪';
      return '📚';
    },
    getResultMessage() {
      const percent = (this.score / this.items.length) * 100;
      if (percent === 100) return '完美！你是垃圾分类大师！';
      if (percent >= 80) return '太棒了！你对垃圾分类很熟悉！';
      if (percent >= 60) return '不错！继续努力学习垃圾分类知识！';
      if (percent >= 40) return '还需要加油！多了解一些分类知识吧！';
      return '加油！垃圾分类需要多多练习哦！';
    }
  }
};
</script>

<style scoped>
/* 滚动容器 */
.waste-sorting-wrapper {
  max-height: 90vh;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px 10px;
  /* 自定义滚动条样式 */
  scrollbar-width: thin;
  scrollbar-color: #81c784 #e8f5e9;
}

/* WebKit 浏览器的滚动条样式 */
.waste-sorting-wrapper::-webkit-scrollbar {
  width: 10px;
}

.waste-sorting-wrapper::-webkit-scrollbar-track {
  background: #e8f5e9;
  border-radius: 10px;
}

.waste-sorting-wrapper::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #66bb6a 0%, #81c784 100%);
  border-radius: 10px;
  border: 2px solid #e8f5e9;
}

.waste-sorting-wrapper::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #4caf50 0%, #66bb6a 100%);
}

.waste-sorting-game {
  max-width: 600px;
  margin: 0 auto;
  padding: 32px;
  background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(76, 175, 80, 0.15);
  position: relative;
  min-height: 500px;
}

/* 头部样式 */
.header {
  margin-bottom: 32px;
}

.header h2 {
  color: #2e7d32;
  font-size: 2em;
  margin: 0 0 20px 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05);
}

/* 进度条 */
.progress-bar {
  position: relative;
  width: 100%;
  height: 32px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.1);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #66bb6a 0%, #81c784 100%);
  border-radius: 16px;
  transition: width 0.5s ease;
  box-shadow: 0 0 10px rgba(102, 187, 106, 0.5);
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #2e7d32;
  font-weight: bold;
  font-size: 0.95em;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

/* 游戏内容 */
.game-content {
  position: relative;
}

/* 物品卡片 */
.item-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 28px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.item-card.shake {
  animation: shake 0.5s;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
  20%, 40%, 60%, 80% { transform: translateX(8px); }
}

.waste-img-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 16px;
}

.waste-img {
  font-size: 80px;
  animation: bounce 1s ease infinite;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.item-name {
  font-size: 1.5em;
  color: #1b5e20;
  font-weight: bold;
  margin: 12px 0;
}

.item-hint {
  color: #66bb6a;
  font-size: 1em;
  margin: 8px 0 0 0;
}

/* 垃圾桶容器 */
.bins-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.bin-btn {
  background: white;
  border: 3px solid #e8f5e9;
  border-radius: 16px;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.bin-btn:hover:not(.disabled) {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.25);
  border-color: #81c784;
}

.bin-btn:active:not(.disabled) {
  transform: translateY(-2px);
}

.bin-btn.selected {
  border-color: #4caf50;
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  animation: pulse 0.6s;
}

.bin-btn.wrong {
  opacity: 0.4;
}

.bin-btn.disabled {
  cursor: not-allowed;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.bin-icon {
  font-size: 48px;
  margin-bottom: 8px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.bin-label {
  font-size: 1em;
  color: #2e7d32;
  font-weight: 600;
}

/* 反馈卡片 */
.feedback-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.feedback-card.correct {
  border-left: 5px solid #4caf50;
  background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e9 100%);
}

.feedback-card.wrong {
  border-left: 5px solid #ff5252;
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
}

.feedback-icon {
  font-size: 48px;
  margin-bottom: 12px;
  animation: zoomIn 0.4s;
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.3);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.feedback-message {
  font-size: 1.3em;
  font-weight: bold;
  margin: 12px 0;
  color: #1b5e20;
}

.knowledge-text {
  font-size: 1em;
  color: #555;
  line-height: 1.6;
  text-align: left;
  background: rgba(255, 255, 255, 0.7);
  padding: 12px;
  border-radius: 8px;
  margin: 16px 0;
}

.knowledge-icon {
  margin-right: 8px;
}

.next-btn {
  background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 14px 32px;
  font-size: 1.1em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
  margin-top: 12px;
}

.next-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

.next-btn:active {
  transform: translateY(0);
}

/* 得分徽章 */
.score-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  background: linear-gradient(135deg, #ffd54f 0%, #ffb300 100%);
  border-radius: 50%;
  width: 80px;
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(255, 179, 0, 0.4);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.score-label {
  font-size: 0.75em;
  color: #f57f17;
  font-weight: bold;
}

.score-value {
  font-size: 2em;
  color: white;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

/* 结果区域 */
.result-area {
  text-align: center;
  padding: 40px 20px;
  animation: fadeIn 0.5s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.result-icon {
  font-size: 100px;
  margin-bottom: 24px;
  animation: zoomIn 0.6s;
}

.result-title {
  color: #2e7d32;
  font-size: 2.2em;
  margin: 20px 0;
}

.final-score {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 8px;
  margin: 24px 0;
}

.score-text {
  font-size: 1.2em;
  color: #558b2f;
}

.score-number {
  font-size: 4em;
  font-weight: bold;
  color: #4caf50;
  text-shadow: 2px 2px 8px rgba(76, 175, 80, 0.3);
}

.score-total {
  font-size: 2em;
  color: #81c784;
}

.result-message {
  font-size: 1.2em;
  color: #558b2f;
  margin: 20px 0;
  line-height: 1.6;
}

.restart-btn {
  background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
  color: white;
  border: none;
  border-radius: 16px;
  padding: 16px 40px;
  font-size: 1.2em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
  margin-top: 20px;
}

.restart-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.4);
}

.restart-btn:active {
  transform: translateY(-1px);
}

/* 过渡动画 */
.feedback-slide-enter-active {
  animation: slideDown 0.4s ease-out;
}

.feedback-slide-leave-active {
  animation: slideUp 0.3s ease-in;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-20px);
  }
}

.result-fade-enter-active {
  animation: fadeIn 0.6s;
}

.result-fade-leave-active {
  animation: fadeOut 0.3s;
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .waste-sorting-wrapper {
    max-height: 95vh;
    padding: 10px 5px;
  }

  .waste-sorting-game {
    max-width: 95vw;
    padding: 20px;
    margin: 10px auto;
  }

  .header h2 {
    font-size: 1.5em;
  }

  .waste-img {
    font-size: 60px;
  }

  .item-name {
    font-size: 1.2em;
  }

  .bins-container {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .bin-btn {
    padding: 16px;
  }

  .bin-icon {
    font-size: 40px;
  }

  .score-badge {
    width: 60px;
    height: 60px;
    top: 10px;
    right: 10px;
  }

  .score-value {
    font-size: 1.5em;
  }

  .score-label {
    font-size: 0.65em;
  }

  .result-icon {
    font-size: 80px;
  }

  .score-number {
    font-size: 3em;
  }
}

@media (max-width: 480px) {
  .waste-sorting-wrapper {
    max-height: 98vh;
    padding: 5px 2px;
  }

  .waste-sorting-wrapper::-webkit-scrollbar {
    width: 6px;
  }

  .waste-sorting-game {
    padding: 16px;
  }

  .item-card {
    padding: 20px;
  }

  .feedback-card {
    padding: 16px;
  }

  .next-btn {
    padding: 12px 24px;
    font-size: 1em;
  }

  .restart-btn {
    padding: 14px 32px;
    font-size: 1.1em;
  }
}
</style>
