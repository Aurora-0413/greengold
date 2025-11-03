<template>
  <div class="quiz-container">
    <div class="quiz-header">
      <h1>智能答题</h1>
      <div class="mode-selector">
        <button 
          :class="['mode-btn', { active: mode === 'practice' }]" 
          @click="switchMode('practice')"
        >
          练习模式
        </button>
        <button 
          :class="['mode-btn', { active: mode === 'challenge' }]" 
          @click="switchMode('challenge')"
        >
          挑战模式
        </button>
      </div>
    </div>

    <!-- 练习模式 -->
    <div v-if="mode === 'practice'" class="practice-mode">
      <div v-if="currentQuestion" class="question-card">
        <h2 class="question-text">{{ parseQuestion(currentQuestion.question).title }}</h2>
        <div class="options">
          <label v-for="opt in parseQuestion(currentQuestion.question).options" :key="opt.key" class="option-item">
            <input 
              type="radio" 
              :value="opt.key"
              v-model="selectedAnswer"
              :disabled="showExplanation"
            >
            <span class="option-key">{{ opt.key }}.</span>
            <span class="option-text">{{ opt.text }}</span>
          </label>
        </div>
        <button 
          class="submit-btn" 
          @click="submitPracticeAnswer"
          :disabled="!selectedAnswer || showExplanation"
        >
          提交答案
        </button>
        
        <div v-if="showExplanation" class="explanation">
          <div class="result" :class="isCorrect ? 'correct' : 'incorrect'">
            {{ isCorrect ? '回答正确！' : '回答错误！' }}
          </div>
          <div class="correct-answer">
            正确答案：{{ currentQuestion.correct_answer }}
          </div>
          <div class="explanation-text">
            {{ currentQuestion.explanation }}
          </div>
          <button class="next-btn" @click="nextQuestion">下一题</button>
        </div>
      </div>
      <div v-else class="loading">
        加载题目中...
      </div>
    </div>

    <!-- 挑战模式 -->
    <div v-else-if="mode === 'challenge'" class="challenge-mode">
      <div v-if="!quizStarted" class="start-screen">
        <h2>挑战模式</h2>
        <p>10道题目，答完后查看成绩</p>
        <button class="start-btn" @click="startQuiz">开始答题</button>
      </div>

      <div v-else-if="!quizSubmitted" class="quiz-questions">
        <!-- 答题卡 -->
        <div class="answer-sheet">
          <h3>答题卡</h3>
          <div class="answer-grid">
            <div 
              v-for="(answer, index) in quizAnswers" 
              :key="index"
              :class="['answer-box', { 
                'answered': answer !== '', 
                'current': index === currentQuestionIndex 
              }]"
              @click="jumpToQuestion(index)"
            >
              {{ index + 1 }}
            </div>
          </div>
        </div>

        <div class="progress">
          题目 {{ currentQuestionIndex + 1 }}/{{ quizQuestions.length }}
        </div>
        
        <div class="question-card">
          <h2 class="question-text">{{ parseQuestion(currentQuizQuestion.question).title }}</h2>
          <div class="options">
            <label v-for="opt in parseQuestion(currentQuizQuestion.question).options" :key="opt.key" class="option-item">
              <input 
                type="radio" 
                :value="opt.key"
                v-model="quizAnswers[currentQuestionIndex]"
              >
              <span class="option-key">{{ opt.key }}.</span>
              <span class="option-text">{{ opt.text }}</span>
            </label>
          </div>
          
          <div class="navigation-buttons">
            <button 
              class="nav-btn" 
              @click="prevQuestion" 
              :disabled="currentQuestionIndex === 0"
            >
              上一题
            </button>
            <button 
              class="nav-btn" 
              @click="nextQuizQuestion" 
              :disabled="currentQuestionIndex === quizQuestions.length - 1"
            >
              下一题
            </button>
          </div>
          
          <button 
            class="submit-quiz-btn" 
            @click="confirmSubmitQuiz"
          >
            提交答卷
          </button>
        </div>
      </div>

      <div v-else class="quiz-results">
        <div class="results-header">
          <h2>答题结果</h2>
          <div class="score">
            得分：{{ quizScore }}分
            (<span>{{ correctCount }}/{{ quizQuestions.length }}</span>)
          </div>
        </div>
        
        <div class="results-container">
          <div class="results-list">
            <div 
              v-for="(result, index) in quizResults" 
              :key="index"
              class="result-item"
            >
              <h3>第 {{ index + 1 }} 题</h3>
              <p>{{ result.question }}</p>
              <div class="answer-info">
                <p>你的答案：<span :class="result.is_correct ? 'correct' : 'incorrect'">
                  {{ result.user_answer }}
                </span></p>
                <p>正确答案：{{ result.correct_answer }}</p>
              </div>
              <div class="explanation">
                {{ result.explanation }}
              </div>
            </div>
          </div>
        </div>
        
        <button class="restart-btn" @click="restartQuiz">
          再来一次
        </button>
      </div>
    </div>

    <button class="back-btn" @click="goBack">返回</button>

    <!-- 自定义确认弹窗 -->
    <div v-if="showConfirmModal" class="confirm-modal" @click="closeConfirmModal">
      <div class="confirm-content" @click.stop>
        <div class="confirm-icon">⚠️</div>
        <h3>确认提交？</h3>
        <p class="confirm-message">
          还有 <span class="highlight">{{ unansweredCount }}</span> 道题目未作答<br>
          未作答的题目将按<span class="highlight">答案错误</span>处理
        </p>
        <div class="confirm-buttons">
          <button class="cancel-btn" @click="closeConfirmModal">继续答题</button>
          <button class="submit-confirm-btn" @click="confirmSubmit">确认提交</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE = '/api' 

export default {
  name: 'QuizPage',
  data() {
    return {
      mode: 'practice',
      // 练习模式
      currentQuestion: null,
      selectedAnswer: '',
      showExplanation: false,
      isCorrect: false,
      // 挑战模式
      quizStarted: false,
      quizSubmitted: false,
      quizId: null,
      quizQuestions: [],
      quizAnswers: [],
      currentQuestionIndex: 0,
      quizScore: 0,
      correctCount: 0,
      quizResults: [],
      // 确认弹窗
      showConfirmModal: false
    }
  },
  computed: {
    currentQuizQuestion() {
      return this.quizQuestions[this.currentQuestionIndex] || {}
    },
    unansweredCount() {
      return this.quizAnswers.filter(answer => answer === '').length
    }
  },
  methods: {
    // 解析题目,分离题干和选项
    parseQuestion(questionText) {
      if (!questionText) return { title: '', options: [] }
      
      const lines = questionText.split('\n')
      const title = lines[0] // 第一行是题干
      const options = []
      
      // 解析选项 (A. B. C. D.)
      for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim()
        if (line) {
          const match = line.match(/^([A-D])\.\s*(.+)$/)
          if (match) {
            options.push({
              key: match[1],
              text: match[2]
            })
          }
        }
      }
      
      return { title, options }
    },
    async switchMode(newMode) {
      this.mode = newMode
      if (newMode === 'practice') {
        this.resetPractice()
        await this.fetchPracticeQuestion()
      } else {
        this.resetChallenge()
      }
    },
    // 练习模式方法
    async fetchPracticeQuestion() {
      try {
        const response = await fetch(`${API_BASE}/practice/question`)
        const data = await response.json()
        if (data.success) {
          this.currentQuestion = data.data
          this.selectedAnswer = ''
          this.showExplanation = false
        }
      } catch (error) {
        console.error('获取题目失败:', error)
      }
    },
    async submitPracticeAnswer() {
      if (!this.selectedAnswer) return
      
      try {
        const response = await fetch(`${API_BASE}/practice/check`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            question_id: this.currentQuestion.id,
            user_answer: this.selectedAnswer
          })
        })
        
        const data = await response.json()
        if (data.success) {
          this.isCorrect = data.data.is_correct
          this.showExplanation = true
        }
      } catch (error) {
        console.error('提交答案失败:', error)
      }
    },
    async nextQuestion() {
      await this.fetchPracticeQuestion()
    },
    resetPractice() {
      this.currentQuestion = null
      this.selectedAnswer = ''
      this.showExplanation = false
      this.isCorrect = false
    },
    // 挑战模式方法
    async startQuiz() {
      try {
        const response = await fetch(`${API_BASE}/quiz/start`)
        const data = await response.json()
        if (data.success) {
          this.quizId = data.data.quiz_id
          this.quizQuestions = data.data.questions
          // 初始化为空字符串数组，而不是 undefined
          this.quizAnswers = new Array(this.quizQuestions.length).fill('')
          this.quizStarted = true
          this.currentQuestionIndex = 0
        }
      } catch (error) {
        console.error('开始测试失败:', error)
      }
    },
    prevQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
      }
    },
    nextQuizQuestion() {
      if (this.currentQuestionIndex < this.quizQuestions.length - 1) {
        this.currentQuestionIndex++
      }
    },
    jumpToQuestion(index) {
      this.currentQuestionIndex = index
    },
    confirmSubmitQuiz() {
      // 检查是否有未答题
      if (this.unansweredCount > 0) {
        this.showConfirmModal = true
      } else {
        this.submitQuiz()
      }
    },
    closeConfirmModal() {
      this.showConfirmModal = false
    },
    confirmSubmit() {
      this.showConfirmModal = false
      this.submitQuiz()
    },
    async submitQuiz() {
      try {
        // 直接提交答案数组（空字符串表示未答题，后端会判定为错误）
        const response = await fetch(`${API_BASE}/quiz/submit`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            quiz_id: this.quizId,
            answers: this.quizAnswers
          })
        })
        
        const data = await response.json()
        if (data.success) {
          this.quizSubmitted = true
          this.quizScore = data.data.score
          this.correctCount = data.data.correct_count
          this.quizResults = data.data.results
        }
      } catch (error) {
        console.error('提交测试失败:', error)
      }
    },
    restartQuiz() {
      this.resetChallenge()
    },
    resetChallenge() {
      this.quizStarted = false
      this.quizSubmitted = false
      this.quizId = null
      this.quizQuestions = []
      this.quizAnswers = []
      this.currentQuestionIndex = 0
      this.quizScore = 0
      this.correctCount = 0
      this.quizResults = []
    },
    // 通用方法
    goBack() {
      this.$router.push('/main')
    }
  },
  async mounted() {
    if (this.mode === 'practice') {
      await this.fetchPracticeQuestion()
    }
  }
}
</script>

<style scoped>
.quiz-container {
  min-height: 100vh;
  height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  overflow-y: auto;
  overflow-x: hidden;
}

.quiz-header {
  text-align: center;
  margin-bottom: 2rem;
}

.quiz-header h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.mode-selector {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.mode-btn {
  padding: 0.8rem 1.5rem;
  border: 2px solid #4CAF50;
  background: white;
  color: #4CAF50;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.mode-btn.active {
  background: #4CAF50;
  color: white;
}

.question-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 0 auto;
}

/* 挑战模式时，题目卡片居中显示 */
.quiz-questions .question-card {
  max-width: 700px;
  margin: 0 auto;
  margin-right: 140px;
}

@media (min-width: 1400px) {
  .quiz-questions .question-card {
    max-width: 900px;
  }
}

.question-card h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  white-space: pre-line;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.option-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-item:hover {
  background: #f8f9fa;
  border-color: #4CAF50;
}

.option-item input[type="radio"] {
  margin-top: 0.25rem;
  flex-shrink: 0;
}

.option-key {
  font-weight: bold;
  color: #4CAF50;
  min-width: 1.5rem;
  flex-shrink: 0;
}

.option-text {
  flex: 1;
  line-height: 1.5;
}

.question-text {
  font-size: 1.3rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  color: #333;
}

/* 挑战模式开始界面 */
.start-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
  padding: 3rem 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.start-screen h2 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.start-screen p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.submit-btn, .next-btn, .start-btn, .submit-quiz-btn, .restart-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  width: 100%;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.restart-btn {
  flex-shrink: 0;
  margin-top: 0;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.explanation {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #ddd;
}

.result {
  font-weight: bold;
  margin-bottom: 1rem;
}

.result.correct {
  color: #4CAF50;
}

.result.incorrect {
  color: #f44336;
}

.correct-answer {
  color: #4CAF50;
  margin-bottom: 1rem;
}

.explanation-text {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
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
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #4CAF50;
  color: white;
}

.progress {
  text-align: center;
  color: #666;
  margin-bottom: 1rem;
}

/* 答题卡样式 */
.answer-sheet {
  position: fixed;
  top: 6rem;
  right: 2rem;
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
  min-width: 200px;
}

.answer-sheet h3 {
  font-size: 1rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  text-align: center;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 0.5rem;
}

.answer-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
}

.answer-box {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  background: #f5f5f5;
  color: #999;
}

.answer-box:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.answer-box.answered {
  background: #c8e6c9;
  color: #2e7d32;
  border-color: #4CAF50;
}

.answer-box.current {
  border-color: #2196F3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.3);
}

/* 移动端隐藏答题卡 */
@media (max-width: 768px) {
  .answer-sheet {
    display: none;
  }
}

.navigation-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.nav-btn {
  flex: 1;
  padding: 0.8rem;
  border: 2px solid #4CAF50;
  background: white;
  color: #4CAF50;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  outline: none;
}

.nav-btn:focus {
  outline: none;
  border-color: #4CAF50;
}

.nav-btn:disabled {
  border-color: #ccc;
  color: #ccc;
  cursor: not-allowed;
}

.nav-btn:hover:not(:disabled) {
  background: #4CAF50;
  color: white;
}

.submit-quiz-btn {
  flex: 2;
  padding: 0.8rem;
  border: 2px solid #4CAF50;
  background: #4CAF50;
  color: white;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  width: 100%;
  margin-top: 1rem;
  outline: none;
}

.submit-quiz-btn:focus {
  outline: none;
  border-color: #4CAF50;
}

.submit-quiz-btn:hover {
  background: #45a049;
  border-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
}

.quiz-results {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 4rem);
  padding-bottom: 1rem;
}

.results-header {
  flex-shrink: 0;
  margin-bottom: 1rem;
}

.results-header h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.score {
  text-align: center;
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 0;
}

.results-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 0.5rem;
  margin-bottom: 1rem;
}

/* 自定义滚动条样式 */
.results-container::-webkit-scrollbar {
  width: 8px;
}

.results-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.results-container::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 4px;
}

.results-container::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding-bottom: 1rem;
}

.result-item {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.result-item h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.answer-info {
  margin: 1rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.answer-info .correct {
  color: #4CAF50;
  font-weight: bold;
}

.answer-info .incorrect {
  color: #f44336;
  font-weight: bold;
}

/* 自定义滚动条样式 */
.quiz-container::-webkit-scrollbar {
  width: 8px;
}

.quiz-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

.quiz-container::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 4px;
}

.quiz-container::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

@media (max-width: 768px) {
  .quiz-container {
    padding: 1rem;
    padding-top: 4rem;
  }

  /* 移动端问题卡片恢复居中，不受答题卡影响 */
  .quiz-questions .question-card {
    max-width: 100%;
    margin: 0 auto;
  }
  
  .quiz-header h1 {
    font-size: 1.5rem;
    margin-bottom: 0.8rem;
  }

  .mode-selector {
    gap: 0.5rem;
    margin-bottom: 1.5rem;
  }

  .mode-btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }

  .question-card {
    padding: 1.5rem 1rem;
    margin-bottom: 1rem;
  }

  .question-text {
    font-size: 1.1rem;
    line-height: 1.5;
  }

  .option-item {
    padding: 0.6rem;
    font-size: 0.95rem;
  }

  .option-text {
    line-height: 1.4;
  }
  
  .back-btn {
    top: 1rem;
    left: 1rem;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }

  .progress {
    font-size: 1rem;
    margin-bottom: 1rem;
    font-weight: bold;
  }
  
  /* 移动端导航按钮布局 */
  .navigation-buttons {
    flex-direction: row;
    gap: 0.5rem;
    margin-top: 1rem;
    flex-wrap: wrap;
  }

  .nav-btn {
    flex: 1;
    min-width: calc(50% - 0.25rem);
    padding: 0.7rem 0.5rem;
    font-size: 0.9rem;
    background: white;
    color: #4CAF50;
    border: 2px solid #4CAF50;
    outline: none;
  }

  /* 移除移动端按钮的悬停效果 */
  .nav-btn:hover:not(:disabled) {
    background: white;
    color: #4CAF50;
    border-color: #4CAF50;
    transform: none;
  }

  .nav-btn:focus:not(:disabled) {
    outline: none;
    border-color: #4CAF50;
    background: white;
  }

  .nav-btn:active:not(:disabled) {
    background: #f0f0f0;
    border-color: #4CAF50;
  }

  /* 提交按钮移到右上角 */
  .submit-quiz-btn {
    position: fixed;
    top: 1rem;
    right: 1rem;
    width: auto;
    min-width: 85px;
    padding: 0.65rem 1.2rem;
    font-size: 0.9rem;
    background: #4CAF50;
    color: white;
    z-index: 1000;
    margin-top: 0;
    flex: none;
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.4);
    outline: none;
    border: 2px solid #4CAF50;
  }

  .submit-quiz-btn:focus {
    outline: none;
    border-color: #4CAF50;
  }

  .submit-quiz-btn:active {
    transform: scale(0.98);
    box-shadow: 0 1px 4px rgba(76, 175, 80, 0.4);
    border-color: #4CAF50;
  }

  /* 练习模式按钮 */
  .submit-btn, .next-btn, .start-btn, .restart-btn {
    padding: 0.8rem;
    font-size: 0.95rem;
  }

  /* 结果页面 */
  .quiz-results {
    padding: 0 0.5rem;
    height: calc(100vh - 2rem);
  }

  .results-header h2 {
    font-size: 1.3rem;
    margin-bottom: 0.8rem;
  }

  .score {
    font-size: 1.2rem;
    margin: 0;
  }

  .results-container {
    padding-right: 0.25rem;
  }

  .results-container::-webkit-scrollbar {
    width: 6px;
  }

  .result-item {
    padding: 1rem;
    margin-bottom: 0;
  }

  .result-item h3 {
    font-size: 1rem;
  }

  .result-item p {
    font-size: 0.9rem;
    line-height: 1.4;
  }

  .answer-info {
    padding: 0.8rem;
    font-size: 0.9rem;
  }

  .explanation {
    font-size: 0.9rem;
    line-height: 1.5;
  }
}

/* 自定义确认弹窗样式 */
.confirm-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.confirm-content {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  max-width: 450px;
  width: 90%;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.confirm-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: bounce 0.6s ease;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.confirm-content h3 {
  color: #2c3e50;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.confirm-message {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 2rem;
}

.confirm-message .highlight {
  color: #f44336;
  font-weight: bold;
  font-size: 1.2rem;
}

.confirm-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.cancel-btn,
.submit-confirm-btn {
  flex: 1;
  padding: 0.9rem 1.5rem;
  border: none;
  border-radius: 25px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
  border: 2px solid #ddd;
}

.cancel-btn:hover {
  background: #e0e0e0;
  border-color: #bbb;
  transform: translateY(-2px);
}

.submit-confirm-btn {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: 2px solid #4CAF50;
}

.submit-confirm-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.cancel-btn:active,
.submit-confirm-btn:active {
  transform: translateY(0);
}

/* 移动端弹窗适配 */
@media (max-width: 768px) {
  .confirm-content {
    padding: 2rem 1.5rem;
    max-width: 90%;
  }

  .confirm-icon {
    font-size: 3rem;
  }

  .confirm-content h3 {
    font-size: 1.5rem;
  }

  .confirm-message {
    font-size: 1rem;
  }

  .confirm-buttons {
    flex-direction: column;
  }

  .cancel-btn,
  .submit-confirm-btn {
    width: 100%;
  }
}
</style>