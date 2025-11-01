<template>
  <div class="carbon-calculator">
    <button class="back-btn" @click="goBack">← 返回</button>
    
    <div class="header">
      <h1>🌱 碳足迹计算器</h1>
      <p class="subtitle">计算您的日常活动产生的碳排放，了解如何减少碳足迹</p>
    </div>

    <div class="calculator-container">
      <!-- 计算表单 -->
      <div class="calculation-form">
        <h2>选择您的活动</h2>
        
        <div class="activity-section">
          <h3>🚗 出行方式</h3>
          <div class="input-group">
            <label>
              <span>开车通勤（公里）</span>
              <input 
                type="number" 
                v-model.number="activities.driving" 
                min="0" 
                placeholder="0"
                @input="calculate"
              >
            </label>
            <div class="carbon-value">≈ {{ (activities.driving * 0.2).toFixed(2) }} kg CO₂</div>
          </div>

          <div class="input-group">
            <label>
              <span>公交/地铁（公里）</span>
              <input 
                type="number" 
                v-model.number="activities.publicTransit" 
                min="0" 
                placeholder="0"
                @input="calculate"
              >
            </label>
            <div class="carbon-value">≈ {{ (activities.publicTransit * 0.05).toFixed(2) }} kg CO₂</div>
          </div>

          <div class="input-group">
            <label>
              <span>骑行/步行（公里）</span>
              <input 
                type="number" 
                v-model.number="activities.cycling" 
                min="0" 
                placeholder="0"
                @input="calculate"
              >
            </label>
            <div class="carbon-value green">≈ 0 kg CO₂ ✓</div>
          </div>
        </div>

        <div class="activity-section">
          <h3>🍔 饮食习惯</h3>
          <div class="input-group">
            <label>
              <span>肉类餐（次/周）</span>
              <input 
                type="number" 
                v-model.number="activities.meatMeals" 
                min="0" 
                placeholder="0"
                @input="calculate"
              >
            </label>
            <div class="carbon-value">≈ {{ (activities.meatMeals * 2.5).toFixed(2) }} kg CO₂</div>
          </div>

          <div class="input-group">
            <label>
              <span>素食餐（次/周）</span>
              <input 
                type="number" 
                v-model.number="activities.vegetarianMeals" 
                min="0" 
                placeholder="0"
                @input="calculate"
              >
            </label>
            <div class="carbon-value">≈ {{ (activities.vegetarianMeals * 0.5).toFixed(2) }} kg CO₂</div>
          </div>

          <div class="input-group">
            <label>
              <span>外卖订单（次/周）</span>
              <input 
                type="number" 
                v-model.number="activities.takeout" 
                min="0" 
                placeholder="0"
                @input="calculate"
              >
            </label>
            <div class="carbon-value">≈ {{ (activities.takeout * 0.8).toFixed(2) }} kg CO₂</div>
          </div>
        </div>

        <div class="activity-section">
          <h3>⚡ 能源使用</h3>
          <div class="input-group">
            <label>
              <span>用电量（度/月）</span>
              <input 
                type="number" 
                v-model.number="activities.electricity" 
                min="0" 
                placeholder="0"
                @input="calculate"
              >
            </label>
            <div class="carbon-value">≈ {{ (activities.electricity * 0.785).toFixed(2) }} kg CO₂</div>
          </div>

          <div class="input-group">
            <label>
              <span>天然气（立方米/月）</span>
              <input 
                type="number" 
                v-model.number="activities.gas" 
                min="0" 
                placeholder="0"
                @input="calculate"
              >
            </label>
            <div class="carbon-value">≈ {{ (activities.gas * 2.1).toFixed(2) }} kg CO₂</div>
          </div>
        </div>

        <div class="activity-section">
          <h3>🛍️ 消费习惯</h3>
          <div class="input-group">
            <label>
              <span>网购次数（次/月）</span>
              <input 
                type="number" 
                v-model.number="activities.shopping" 
                min="0" 
                placeholder="0"
                @input="calculate"
              >
            </label>
            <div class="carbon-value">≈ {{ (activities.shopping * 0.5).toFixed(2) }} kg CO₂</div>
          </div>
        </div>

        <button class="reset-btn" @click="resetForm">🔄 重置</button>
      </div>

      <!-- 结果展示 -->
      <div class="results-panel">
        <div class="total-carbon">
          <div class="carbon-icon">🌍</div>
          <h3>总碳排放量</h3>
          <div class="total-value">{{ totalCarbon.toFixed(2) }}</div>
          <div class="unit">千克 CO₂</div>
          <div class="level-badge" :class="carbonLevel.class">
            {{ carbonLevel.text }}
          </div>
        </div>

        <div class="equivalents">
          <h3>等效于：</h3>
          <div class="equivalent-item">
            <span class="emoji">🌳</span>
            <span class="text">需要种植 <strong>{{ treesNeeded }}</strong> 棵树来抵消</span>
          </div>
          <div class="equivalent-item">
            <span class="emoji">🚗</span>
            <span class="text">相当于开车行驶 <strong>{{ drivingDistance }}</strong> 公里</span>
          </div>
          <div class="equivalent-item">
            <span class="emoji">💡</span>
            <span class="text">相当于 <strong>{{ lightBulbHours }}</strong> 小时灯泡用电</span>
          </div>
        </div>

        <div class="recommendations">
          <h3>💡 减碳建议</h3>
          <div class="tip-list">
            <div class="tip-item" v-for="(tip, index) in recommendations" :key="index">
              <span class="tip-icon">✓</span>
              <span class="tip-text">{{ tip }}</span>
            </div>
          </div>
        </div>

        <button class="share-btn" @click="generatePoster">
          📤 生成分享海报
        </button>
      </div>
    </div>

    <!-- 海报弹窗 -->
    <div v-if="showPoster" class="poster-modal" @click="closePoster">
      <div class="poster-content" @click.stop>
        <button class="close-button" @click="closePoster">×</button>
        <div class="poster" ref="poster">
          <div class="poster-header">
            <h2>🌱 我的碳足迹</h2>
            <p>绿水青山就是金山银山</p>
          </div>
          <div class="poster-body">
            <div class="poster-carbon">
              <div class="poster-value">{{ totalCarbon.toFixed(2) }}</div>
              <div class="poster-unit">kg CO₂</div>
            </div>
            <div class="poster-level" :class="carbonLevel.class">
              {{ carbonLevel.text }}
            </div>
            <div class="poster-trees">
              需要种植 {{ treesNeeded }} 棵树来抵消
            </div>
          </div>
          <div class="poster-footer">
            <p>让我们一起为地球减负 🌍</p>
            <p class="poster-date">{{ currentDate }}</p>
          </div>
        </div>
        <p class="poster-hint">长按图片保存到相册</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CarbonCalculator',
  data() {
    return {
      activities: {
        driving: 0,
        publicTransit: 0,
        cycling: 0,
        meatMeals: 0,
        vegetarianMeals: 0,
        takeout: 0,
        electricity: 0,
        gas: 0,
        shopping: 0
      },
      totalCarbon: 0,
      showPoster: false
    }
  },
  computed: {
    treesNeeded() {
      // 一棵树每年吸收约22kg CO2
      return Math.ceil(this.totalCarbon / 22)
    },
    drivingDistance() {
      // 每公里约0.2kg CO2
      return Math.round(this.totalCarbon / 0.2)
    },
    lightBulbHours() {
      // 60W灯泡每小时约0.05kg CO2
      return Math.round(this.totalCarbon / 0.05)
    },
    carbonLevel() {
      if (this.totalCarbon === 0) {
        return { text: '未计算', class: 'level-none' }
      } else if (this.totalCarbon < 50) {
        return { text: '低碳生活 ⭐⭐⭐', class: 'level-low' }
      } else if (this.totalCarbon < 100) {
        return { text: '中等水平 ⭐⭐', class: 'level-medium' }
      } else {
        return { text: '需要改善 ⭐', class: 'level-high' }
      }
    },
    recommendations() {
      const tips = []
      if (this.activities.driving > 20) {
        tips.push('尝试使用公共交通或拼车，减少私家车使用')
      }
      if (this.activities.meatMeals > 7) {
        tips.push('适当增加素食比例，每周至少2天无肉日')
      }
      if (this.activities.takeout > 5) {
        tips.push('减少外卖订单，自己做饭更健康环保')
      }
      if (this.activities.electricity > 200) {
        tips.push('节约用电，及时关闭不使用的电器')
      }
      if (this.activities.shopping > 10) {
        tips.push('理性消费，减少不必要的网购')
      }
      if (tips.length === 0) {
        tips.push('继续保持绿色生活方式！')
        tips.push('多骑行步行，既健康又环保')
        tips.push('使用可重复利用的购物袋和水杯')
      }
      return tips
    },
    currentDate() {
      const date = new Date()
      return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
    }
  },
  methods: {
    calculate() {
      this.totalCarbon = 
        this.activities.driving * 0.2 +
        this.activities.publicTransit * 0.05 +
        this.activities.meatMeals * 2.5 +
        this.activities.vegetarianMeals * 0.5 +
        this.activities.takeout * 0.8 +
        this.activities.electricity * 0.785 +
        this.activities.gas * 2.1 +
        this.activities.shopping * 0.5
    },
    resetForm() {
      this.activities = {
        driving: 0,
        publicTransit: 0,
        cycling: 0,
        meatMeals: 0,
        vegetarianMeals: 0,
        takeout: 0,
        electricity: 0,
        gas: 0,
        shopping: 0
      }
      this.totalCarbon = 0
    },
    generatePoster() {
      if (this.totalCarbon === 0) {
        alert('请先填写您的活动数据！')
        return
      }
      this.showPoster = true
    },
    closePoster() {
      this.showPoster = false
    },
    goBack() {
      this.$router.push('/main')
    }
  }
}
</script>

<style scoped>
.carbon-calculator {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  position: relative;
}

.back-btn {
  position: fixed;
  top: 2rem;
  left: 2rem;
  background: white;
  border: 2px solid #4CAF50;
  color: #4CAF50;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  z-index: 100;
}

.back-btn:hover {
  background: #4CAF50;
  color: white;
  transform: translateX(-5px);
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.calculator-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.calculation-form {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-height: calc(100vh - 12rem);
  overflow-y: auto;
  overflow-x: hidden;
}

/* 自定义滚动条样式 */
.calculation-form::-webkit-scrollbar {
  width: 8px;
}

.calculation-form::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.calculation-form::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 10px;
  transition: background 0.3s ease;
}

.calculation-form::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

.calculation-form h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.5rem;
}

.activity-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.activity-section:last-of-type {
  border-bottom: none;
}

.activity-section h3 {
  color: #4CAF50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.input-group label span {
  color: #333;
  font-weight: 500;
}

.input-group input {
  width: 120px;
  padding: 0.5rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #4CAF50;
}

.carbon-value {
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.3rem;
  text-align: right;
}

.carbon-value.green {
  color: #4CAF50;
  font-weight: bold;
}

.reset-btn {
  width: 100%;
  padding: 0.8rem;
  background: #f5f5f5;
  border: 2px solid #ddd;
  color: #666;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  background: #e0e0e0;
  border-color: #bbb;
}

.results-panel {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 2rem;
  height: fit-content;
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
  overflow-x: hidden;
}

/* 结果面板滚动条样式 */
.results-panel::-webkit-scrollbar {
  width: 6px;
}

.results-panel::-webkit-scrollbar-track {
  background: transparent;
}

.results-panel::-webkit-scrollbar-thumb {
  background: rgba(76, 175, 80, 0.3);
  border-radius: 10px;
}

.results-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(76, 175, 80, 0.5);
}

.total-carbon {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border-radius: 15px;
  color: white;
  margin-bottom: 2rem;
}

.carbon-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.total-carbon h3 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  opacity: 0.9;
}

.total-value {
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.unit {
  font-size: 1.1rem;
  opacity: 0.9;
}

.level-badge {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  display: inline-block;
}

.level-none {
  background: rgba(255, 255, 255, 0.3);
}

.level-low {
  background: rgba(255, 255, 255, 0.3);
  animation: glow 2s ease-in-out infinite;
}

.level-medium {
  background: rgba(255, 235, 59, 0.3);
}

.level-high {
  background: rgba(244, 67, 54, 0.3);
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 5px rgba(255, 255, 255, 0.5); }
  50% { box-shadow: 0 0 20px rgba(255, 255, 255, 0.8); }
}

.equivalents {
  margin-bottom: 2rem;
}

.equivalents h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.equivalent-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 0.8rem;
}

.equivalent-item .emoji {
  font-size: 1.5rem;
}

.equivalent-item .text {
  color: #666;
  flex: 1;
}

.equivalent-item strong {
  color: #4CAF50;
  font-size: 1.1rem;
}

.recommendations {
  margin-bottom: 2rem;
}

.recommendations h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.tip-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  padding: 0.8rem;
  background: #e8f5e9;
  border-radius: 8px;
  border-left: 3px solid #4CAF50;
}

.tip-icon {
  color: #4CAF50;
  font-weight: bold;
  flex-shrink: 0;
}

.tip-text {
  color: #333;
  line-height: 1.5;
}

.share-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border: none;
  color: white;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.share-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

/* 海报样式 */
.poster-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 2rem;
}

.poster-content {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 400px;
  position: relative;
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: white;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #666;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-button:hover {
  background: #f5f5f5;
  color: #333;
}

.poster {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border-radius: 15px;
  padding: 2rem;
  color: white;
  text-align: center;
}

.poster-header h2 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.poster-header p {
  opacity: 0.9;
  font-size: 1rem;
}

.poster-body {
  padding: 2rem 0;
}

.poster-carbon {
  margin-bottom: 1rem;
}

.poster-value {
  font-size: 4rem;
  font-weight: bold;
  line-height: 1;
}

.poster-unit {
  font-size: 1.2rem;
  opacity: 0.9;
}

.poster-level {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  display: inline-block;
  margin-bottom: 1rem;
  font-weight: bold;
}

.poster-trees {
  font-size: 1.1rem;
  opacity: 0.9;
}

.poster-footer {
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
}

.poster-footer p {
  margin: 0.5rem 0;
}

.poster-date {
  opacity: 0.7;
  font-size: 0.9rem;
}

.poster-hint {
  text-align: center;
  color: #999;
  margin-top: 1rem;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .calculator-container {
    grid-template-columns: 1fr;
  }

  .results-panel {
    position: static;
    max-height: none;
  }

  .calculation-form {
    max-height: none;
  }
}

@media (max-width: 768px) {
  .carbon-calculator {
    padding: 1rem;
  }

  .header h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 0.95rem;
  }

  .calculation-form,
  .results-panel {
    padding: 1.5rem;
  }

  .input-group label {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .input-group input {
    width: 100%;
  }

  .carbon-value {
    text-align: left;
  }

  .back-btn {
    top: 1rem;
    left: 1rem;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }

  .total-value {
    font-size: 2.5rem;
  }

  .poster-content {
    padding: 1rem;
  }

  .poster {
    padding: 1.5rem;
  }

  .poster-value {
    font-size: 3rem;
  }
}
</style>
