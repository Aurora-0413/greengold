<template>
  <div class="knowledge-map">
    <div class="header">
      <button class="back-button" @click="goBack">← 返回</button>
      <h1>两山理论知识体系</h1>
    </div>

    <div class="map-container">
      <svg class="mindmap-svg" viewBox="0 0 1600 1000">
        <!-- 连接线 -->
        <g class="connections">
          <!-- 根节点到一级节点的连接 -->
          <path d="M 250 500 Q 350 300, 450 200" stroke="#4CAF50" stroke-width="3" fill="none" />
          <path d="M 250 500 Q 350 500, 450 500" stroke="#4CAF50" stroke-width="3" fill="none" />
          <path d="M 250 500 Q 350 700, 450 800" stroke="#4CAF50" stroke-width="3" fill="none" />

          <!-- 坚持人与自然和谐共生 的子节点连接 -->
          <path d="M 650 200 L 850 80" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 200 L 850 200" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 200 L 850 320" stroke="#66BB6A" stroke-width="2" fill="none" />

          <!-- 建设美丽中国 的子节点连接 -->
          <path d="M 650 500 L 850 420" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 500 L 850 540" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 500 L 850 660" stroke="#66BB6A" stroke-width="2" fill="none" />

          <!-- 共谋全球生态文明建设之路 的子节点连接 -->
          <path d="M 650 800 L 850 740" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 800 L 850 820" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 800 L 850 900" stroke="#66BB6A" stroke-width="2" fill="none" />
        </g>

        <!-- 根节点 -->
        <g class="node root-node" @click="selectNode('root')">
          <rect x="50" y="460" width="200" height="80" rx="40" />
          <text x="150" y="495" text-anchor="middle">建设社会主</text>
          <text x="150" y="520" text-anchor="middle">义生态文明</text>
        </g>

        <!-- 一级节点 -->
        <g class="node level1-node" @click="selectNode('harmony')">
          <rect x="450" y="160" width="200" height="80" rx="15" />
          <text x="550" y="190" text-anchor="middle">坚持人与自</text>
          <text x="550" y="215" text-anchor="middle">然和谐共生</text>
        </g>

        <g class="node level1-node" @click="selectNode('beautiful')">
          <rect x="450" y="460" width="200" height="80" rx="15" />
          <text x="550" y="495" text-anchor="middle">建设美丽中国</text>
        </g>

        <g class="node level1-node" @click="selectNode('global')">
          <rect x="450" y="760" width="200" height="80" rx="15" />
          <text x="550" y="785" text-anchor="middle">共谋全球生态</text>
          <text x="550" y="810" text-anchor="middle">文明建设之路</text>
        </g>

        <!-- 二级节点 - 坚持人与自然和谐共生 -->
        <g class="node level2-node" @click="selectNode('harmony-1')">
          <rect x="850" y="40" width="300" height="80" rx="15" />
          <text x="1000" y="75" text-anchor="middle">生态兴则文明兴</text>
        </g>

        <g class="node level2-node" @click="selectNode('harmony-2')">
          <rect x="850" y="160" width="350" height="80" rx="15" />
          <text x="1025" y="195" text-anchor="middle">绿水青山就是金山银山</text>
        </g>

        <g class="node level2-node" @click="selectNode('harmony-3')">
          <rect x="850" y="280" width="480" height="80" rx="15" />
          <text x="1090" y="310" text-anchor="middle">把生态文明建设摆在全局</text>
          <text x="1090" y="335" text-anchor="middle">工作的突出位置</text>
        </g>

        <!-- 二级节点 - 建设美丽中国 -->
        <g class="node level2-node" @click="selectNode('beautiful-1')">
          <rect x="850" y="380" width="380" height="80" rx="15" />
          <text x="1040" y="410" text-anchor="middle">加快形成绿色生产方式</text>
          <text x="1040" y="435" text-anchor="middle">和生活方式</text>
        </g>

        <g class="node level2-node" @click="selectNode('beautiful-2')">
          <rect x="850" y="500" width="520" height="80" rx="15" />
          <text x="1110" y="530" text-anchor="middle">坚持山水林田湖草沙一体化</text>
          <text x="1110" y="555" text-anchor="middle">保护和系统治理</text>
        </g>

        <g class="node level2-node" @click="selectNode('beautiful-3')">
          <rect x="850" y="620" width="420" height="80" rx="15" />
          <text x="1060" y="650" text-anchor="middle">用最严格制度最严密法治</text>
          <text x="1060" y="675" text-anchor="middle">保护生态环境</text>
        </g>

        <!-- 二级节点 - 共谋全球生态文明建设之路 -->
        <g class="node level2-node" @click="selectNode('global-1')">
          <rect x="850" y="700" width="280" height="80" rx="15" />
          <text x="990" y="735" text-anchor="middle">保护人类共同家园</text>
        </g>

        <g class="node level2-node" @click="selectNode('global-2')">
          <rect x="850" y="780" width="280" height="80" rx="15" />
          <text x="990" y="815" text-anchor="middle">共建清洁美丽世界</text>
        </g>

        <g class="node level2-node" @click="selectNode('global-3')">
          <rect x="850" y="860" width="350" height="80" rx="15" />
          <text x="1025" y="895" text-anchor="middle">积极推动全球可持续发展</text>
        </g>
      </svg>
    </div>

    <!-- 知识详情弹窗 -->
    <div v-if="selectedNode" class="detail-modal" @click="closeModal">
      <div class="detail-content" @click.stop>
        <button class="close-button" @click="closeModal">×</button>
        <h2>{{ nodeDetails[selectedNode].title }}</h2>
        <div class="detail-body">
          <p>{{ nodeDetails[selectedNode].content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KnowledgeMap',
  data() {
    return {
      selectedNode: null,
      nodeDetails: {
        'root': {
          title: '建设社会主义生态文明',
          content: '生态文明建设是关系中华民族永续发展的根本大计。建设生态文明是实现中华民族伟大复兴的重要战略任务。'
        },
        'harmony': {
          title: '坚持人与自然和谐共生',
          content: '人与自然是生命共同体，人类必须尊重自然、顺应自然、保护自然。'
        },
        'harmony-1': {
          title: '生态兴则文明兴',
          content: '生态环境变化直接影响文明兴衰演替。生态兴则文明兴，生态衰则文明衰。'
        },
        'harmony-2': {
          title: '绿水青山就是金山银山',
          content: '我们既要绿水青山，也要金山银山。宁要绿水青山，不要金山银山，而且绿水青山就是金山银山。'
        },
        'harmony-3': {
          title: '把生态文明建设摆在全局工作的突出位置',
          content: '生态文明建设是"五位一体"总体布局的重要组成部分，必须摆在全局工作的突出地位。'
        },
        'beautiful': {
          title: '建设美丽中国',
          content: '建设美丽中国是全面建设社会主义现代化国家的重要目标。'
        },
        'beautiful-1': {
          title: '加快形成绿色生产方式和生活方式',
          content: '推动形成绿色发展方式和生活方式，是发展观的一场深刻革命。'
        },
        'beautiful-2': {
          title: '坚持山水林田湖草沙一体化保护和系统治理',
          content: '山水林田湖草沙是一个生命共同体，必须统筹兼顾、整体施策、多措并举。'
        },
        'beautiful-3': {
          title: '用最严格制度最严密法治保护生态环境',
          content: '只有实行最严格的制度、最严密的法治，才能为生态文明建设提供可靠保障。'
        },
        'global': {
          title: '共谋全球生态文明建设之路',
          content: '建设绿色家园是人类的共同梦想。国际社会应该携手同行，共谋全球生态文明建设之路。'
        },
        'global-1': {
          title: '保护人类共同家园',
          content: '地球是人类唯一的家园，保护生态环境、应对气候变化需要世界各国同舟共济、共同努力。'
        },
        'global-2': {
          title: '共建清洁美丽世界',
          content: '携手应对全球环境挑战，共同建设清洁美丽的世界。'
        },
        'global-3': {
          title: '积极推动全球可持续发展',
          content: '推动绿色发展，促进人与自然和谐共生，构建人类命运共同体。'
        }
      }
    }
  },
  methods: {
    goBack() {
      this.$router.push('/main')
    },
    selectNode(nodeId) {
      this.selectedNode = nodeId
    },
    closeModal() {
      this.selectedNode = null
    }
  }
}
</script>

<style scoped>
.knowledge-map {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  gap: 2rem;
}

.back-button {
  padding: 0.75rem 1.5rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.back-button:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.header h1 {
  color: #2c3e50;
  font-size: 2rem;
  margin: 0;
}

.map-container {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.mindmap-svg {
  width: 100%;
  height: auto;
  min-height: 800px;
}

/* 节点样式 */
.node {
  cursor: pointer;
  transition: all 0.3s ease;
}

.node rect {
  transition: all 0.3s ease;
}

.node text {
  fill: white;
  font-size: 16px;
  font-weight: 500;
  pointer-events: none;
}

/* 根节点样式 */
.root-node rect {
  fill: #4CAF50;
}

.root-node:hover rect {
  fill: #45a049;
  filter: drop-shadow(0 4px 8px rgba(76, 175, 80, 0.4));
}

/* 一级节点样式 */
.level1-node rect {
  fill: #81C784;
}

.level1-node:hover rect {
  fill: #66BB6A;
  filter: drop-shadow(0 4px 8px rgba(129, 199, 132, 0.4));
}

/* 二级节点样式 */
.level2-node rect {
  fill: white;
  stroke: #4CAF50;
  stroke-width: 2;
}

.level2-node text {
  fill: #2c3e50;
}

.level2-node:hover rect {
  fill: #E8F5E9;
  stroke: #45a049;
  stroke-width: 3;
  filter: drop-shadow(0 4px 8px rgba(76, 175, 80, 0.2));
}

/* 连接线样式 */
.connections path {
  transition: all 0.3s ease;
}

/* 详情弹窗 */
.detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
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

.detail-content {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  position: relative;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 40px;
  height: 40px;
  border: none;
  background: #f44336;
  color: white;
  font-size: 1.5rem;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.close-button:hover {
  background: #d32f2f;
  transform: rotate(90deg);
}

.detail-content h2 {
  color: #4CAF50;
  margin-bottom: 1.5rem;
  padding-right: 3rem;
  font-size: 1.8rem;
}

.detail-body {
  color: #2c3e50;
  line-height: 1.8;
}

.detail-body p {
  font-size: 1.1rem;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .knowledge-map {
    padding: 1rem;
  }

  .header h1 {
    font-size: 1.5rem;
  }

  .mindmap-svg {
    min-height: 400px;
  }

  .node text {
    font-size: 12px;
  }

  .detail-content {
    padding: 1.5rem;
  }

  .detail-content h2 {
    font-size: 1.4rem;
  }

  .detail-body p {
    font-size: 1rem;
  }
}
</style>
