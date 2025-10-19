<template>
  <div class="timeline-container">
    <div class="timeline-header">
      <h1 class="title">安吉之变</h1>
      <p class="subtitle">从矿山小县到绿水青山的蝶变之路</p>
    </div>
    
    <div class="timeline-wrapper">
      <div class="timeline-scroll">
        <div class="timeline-line"></div>
        
        <!-- 2003 关停矿山 -->
        <div class="timeline-item" :class="{ active: activeIndex === 0 }">
          <div class="timeline-dot" @click="openVideo(0)"></div>
          <div class="timeline-content">
            <div class="year">2003</div>
            <div class="event-title">关停矿山</div>
            <div class="event-desc">痛下决心，关停污染矿山（微电影）</div>
            <button class="view-btn" @click="openVideo(0)">查看详情</button>
          </div>
        </div>

        <!-- 2005 理论提出 -->
        <div class="timeline-item" :class="{ active: activeIndex === 1 }">
          <div class="timeline-dot" @click="openVideo(1)"></div>
          <div class="timeline-content">
            <div class="year">2005</div>
            <div class="event-title">理论提出</div>
            <div class="event-desc">"绿水青山就是金山银山"</div>
            <button class="view-btn" @click="openVideo(1)">查看详情</button>
          </div>
        </div>

        <!-- 2010s 生态修复 -->
        <div class="timeline-item" :class="{ active: activeIndex === 2 }">
          <div class="timeline-dot" @click="openVideo(2)"></div>
          <div class="timeline-content">
            <div class="year">2010s</div>
            <div class="event-title">生态修复</div>
            <div class="event-desc">全面推进生态环境治理（微电影）</div>
            <button class="view-btn" @click="openVideo(2)">查看详情</button>
          </div>
        </div>

        <!-- 2021 最佳旅游乡村 -->
        <div class="timeline-item" :class="{ active: activeIndex === 3 }">
          <div class="timeline-dot" @click="openVideo(3)"></div>
          <div class="timeline-content">
            <div class="year">2021</div>
            <div class="event-title">荣获殊荣</div>
            <div class="event-desc">"最佳旅游乡村"</div>
            <button class="view-btn" @click="openVideo(3)">查看详情</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 视频弹窗 -->
    <div class="video-modal" v-if="showVideo" @click="closeVideo">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="closeVideo">&times;</button>
        <div class="video-info">
          <h2>{{ videoData[currentVideoIndex].title }}</h2>
          <p>{{ videoData[currentVideoIndex].description }}</p>
        </div>
        <video 
          ref="videoPlayer"
          :src="videoData[currentVideoIndex].src" 
          controls 
          autoplay
          class="video-player"
        >
          您的浏览器不支持视频播放
        </video>
      </div>
    </div>

    <!-- 返回按钮 -->
    <button class="back-btn" @click="goBack">
      <span>←</span> 返回
    </button>
  </div>
</template>

<script>
export default {
  name: 'AnjiTimeline',
  data() {
    return {
      activeIndex: -1,
      showVideo: false,
      currentVideoIndex: 0,
      videoData: [
        {
          title: '2003年 - 关停矿山',
          description: '安吉县痛下决心，关停了大量污染严重的矿山企业，开始走向绿色发展之路。',
          src: '/videos/2003.mp4' // 请将视频放到 public/videos 文件夹
        },
        {
          title: '2005年 - 理论提出',
          description: '"绿水青山就是金山银山"理念在安吉正式提出，为安吉发展指明方向。',
          src: '/videos/2005.mp4'
        },
        {
          title: '2010年代 - 生态修复',
          description: '全面推进生态环境治理，竹产业转型升级，美丽乡村建设如火如荼。',
          src: '/videos/2010s.mp4'
        },
        {
          title: '2021年 - 最佳旅游乡村',
          description: '安吉余村入选联合国世界旅游组织"最佳旅游乡村"，走向世界舞台。',
          src: '/videos/2021.mp4'
        }
      ]
    }
  },
  methods: {
    openVideo(index) {
      this.currentVideoIndex = index
      this.activeIndex = index
      this.showVideo = true
    },
    closeVideo() {
      this.showVideo = false
      this.activeIndex = -1
      // 停止视频播放
      if (this.$refs.videoPlayer) {
        this.$refs.videoPlayer.pause()
      }
    },
    goBack() {
      this.$router.push('/main')
    }
  }
}
</script>

<style scoped>
.timeline-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  overflow-x: hidden;
  position: relative;
}

.timeline-header {
  text-align: center;
  color: white;
  margin-bottom: 3rem;
  animation: fadeInDown 1s ease;
}

.title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
}

.timeline-wrapper {
  max-width: 900px;
  margin: 0 auto;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 2rem 1rem;
  height: calc(100vh - 250px);
}

.timeline-wrapper::-webkit-scrollbar {
  width: 8px;
}

.timeline-wrapper::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.timeline-wrapper::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
}

.timeline-scroll {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  padding: 2rem 1rem;
  position: relative;
}

.timeline-line {
  position: absolute;
  top: 0;
  left: 50%;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.3) 0%, 
    rgba(255, 255, 255, 0.8) 50%, 
    rgba(255, 255, 255, 0.3) 100%);
  transform: translateX(-50%);
  z-index: 0;
}

.timeline-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 2rem;
  z-index: 1;
  animation: fadeInUp 0.8s ease forwards;
  opacity: 0;
}

.timeline-item:nth-child(2) { animation-delay: 0.2s; }
.timeline-item:nth-child(3) { animation-delay: 0.4s; }
.timeline-item:nth-child(4) { animation-delay: 0.6s; }
.timeline-item:nth-child(5) { animation-delay: 0.8s; }

/* 左右交替布局 */
.timeline-item:nth-child(odd) {
  flex-direction: row;
}

.timeline-item:nth-child(even) {
  flex-direction: row-reverse;
}

.timeline-item:nth-child(odd) .timeline-content {
  margin-left: 2rem;
}

.timeline-item:nth-child(even) .timeline-content {
  margin-right: 2rem;
}

.timeline-dot {
  width: 24px;
  height: 24px;
  background: white;
  border: 4px solid #ffd700;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7);
  animation: pulse 2s infinite;
  z-index: 2;
}

.timeline-item.active .timeline-dot,
.timeline-dot:hover {
  transform: scale(1.5);
  background: #ffd700;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
}

.timeline-content {
  background: rgba(255, 255, 255, 0.95);
  padding: 1.5rem;
  border-radius: 15px;
  flex: 1;
  max-width: 350px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  text-align: center;
}

.timeline-item:hover .timeline-content {
  transform: translateY(-10px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
}

.year {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.event-title {
  font-size: 1.4rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.event-desc {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.view-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.view-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
}

/* 视频弹窗 */
.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 90%;
  max-height: 90%;
  position: relative;
  animation: slideUp 0.3s ease;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #ff4444;
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}

.close-btn:hover {
  background: #cc0000;
  transform: rotate(90deg);
}

.video-info {
  margin-bottom: 1rem;
  text-align: center;
}

.video-info h2 {
  color: #333;
  margin-bottom: 0.5rem;
}

.video-info p {
  color: #666;
  line-height: 1.6;
}

.video-player {
  width: 100%;
  max-width: 800px;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

/* 返回按钮 */
.back-btn {
  position: fixed;
  top: 2rem;
  left: 2rem;
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 100;
}

.back-btn:hover {
  background: white;
  transform: translateX(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

/* 动画 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 215, 0, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 215, 0, 0);
  }
}

/* 移动端适配 */
@media screen and (max-width: 768px) {
  .timeline-container {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .timeline-wrapper {
    padding: 1rem 0.5rem;
    height: calc(100vh - 200px);
  }

  .timeline-scroll {
    gap: 2.5rem;
    padding: 1rem 0.5rem;
  }

  .timeline-line {
    left: 30px;
  }

  /* 移动端全部靠左排列 */
  .timeline-item,
  .timeline-item:nth-child(odd),
  .timeline-item:nth-child(even) {
    flex-direction: row;
    gap: 1rem;
  }

  .timeline-item:nth-child(odd) .timeline-content,
  .timeline-item:nth-child(even) .timeline-content {
    margin-left: 1rem;
    margin-right: 0;
  }

  .timeline-dot {
    flex-shrink: 0;
  }

  .timeline-content {
    max-width: 100%;
    padding: 1rem;
  }

  .year {
    font-size: 1.5rem;
  }

  .event-title {
    font-size: 1.2rem;
  }

  .event-desc {
    font-size: 0.9rem;
  }

  .modal-content {
    padding: 1rem;
    max-width: 95%;
  }

  .video-player {
    max-width: 100%;
  }

  .back-btn {
    top: 1rem;
    left: 1rem;
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
