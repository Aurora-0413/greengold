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
          <path d="M 250 480 Q 350 280, 450 150" stroke="#4CAF50" stroke-width="3" fill="none" />
          <path d="M 250 480 Q 350 480, 450 480" stroke="#4CAF50" stroke-width="3" fill="none" />
          <path d="M 250 480 Q 350 650, 450 780" stroke="#4CAF50" stroke-width="3" fill="none" />

          <!-- 坚持人与自然和谐共生 的子节点连接 -->
          <path d="M 650 150 L 850 40" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 150 L 850 150" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 150 L 850 260" stroke="#66BB6A" stroke-width="2" fill="none" />

          <!-- 建设美丽中国 的子节点连接 -->
          <path d="M 650 480 L 850 360" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 480 L 850 480" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 480 L 850 600" stroke="#66BB6A" stroke-width="2" fill="none" />

          <!-- 共谋全球生态文明建设之路 的子节点连接 -->
          <path d="M 650 780 L 850 710" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 780 L 850 820" stroke="#66BB6A" stroke-width="2" fill="none" />
          <path d="M 650 780 L 850 930" stroke="#66BB6A" stroke-width="2" fill="none" />
        </g>

        <!-- 根节点 -->
        <g class="node root-node" @click="selectNode('root')">
          <rect x="50" y="440" width="200" height="80" rx="40" />
          <text x="150" y="475" text-anchor="middle">建设社会主</text>
          <text x="150" y="500" text-anchor="middle">义生态文明</text>
        </g>

        <!-- 一级节点 -->
        <g class="node level1-node" @click="selectNode('harmony')">
          <rect x="450" y="110" width="200" height="80" rx="15" />
          <text x="550" y="140" text-anchor="middle">坚持人与自</text>
          <text x="550" y="165" text-anchor="middle">然和谐共生</text>
        </g>

        <g class="node level1-node" @click="selectNode('beautiful')">
          <rect x="450" y="440" width="200" height="80" rx="15" />
          <text x="550" y="475" text-anchor="middle">建设美丽中国</text>
        </g>

        <g class="node level1-node" @click="selectNode('global')">
          <rect x="450" y="740" width="200" height="80" rx="15" />
          <text x="550" y="765" text-anchor="middle">共谋全球生态</text>
          <text x="550" y="790" text-anchor="middle">文明建设之路</text>
        </g>

        <!-- 二级节点 - 坚持人与自然和谐共生 -->
        <g class="node level2-node" @click="selectNode('harmony-1')">
          <rect x="850" y="0" width="300" height="80" rx="15" />
          <text x="1000" y="35" text-anchor="middle">生态兴则文明兴</text>
        </g>

        <g class="node level2-node" @click="selectNode('harmony-2')">
          <rect x="850" y="110" width="350" height="80" rx="15" />
          <text x="1025" y="145" text-anchor="middle">绿水青山就是金山银山</text>
        </g>

        <g class="node level2-node" @click="selectNode('harmony-3')">
          <rect x="850" y="220" width="480" height="80" rx="15" />
          <text x="1090" y="250" text-anchor="middle">把生态文明建设摆在全局</text>
          <text x="1090" y="275" text-anchor="middle">工作的突出位置</text>
        </g>

        <!-- 二级节点 - 建设美丽中国 -->
        <g class="node level2-node" @click="selectNode('beautiful-1')">
          <rect x="850" y="320" width="380" height="80" rx="15" />
          <text x="1040" y="350" text-anchor="middle">加快形成绿色生产方式</text>
          <text x="1040" y="375" text-anchor="middle">和生活方式</text>
        </g>

        <g class="node level2-node" @click="selectNode('beautiful-2')">
          <rect x="850" y="440" width="520" height="80" rx="15" />
          <text x="1110" y="470" text-anchor="middle">坚持山水林田湖草沙一体化</text>
          <text x="1110" y="495" text-anchor="middle">保护和系统治理</text>
        </g>

        <g class="node level2-node" @click="selectNode('beautiful-3')">
          <rect x="850" y="560" width="420" height="80" rx="15" />
          <text x="1060" y="590" text-anchor="middle">用最严格制度最严密法治</text>
          <text x="1060" y="615" text-anchor="middle">保护生态环境</text>
        </g>

        <!-- 二级节点 - 共谋全球生态文明建设之路 -->
        <g class="node level2-node" @click="selectNode('global-1')">
          <rect x="850" y="670" width="280" height="80" rx="15" />
          <text x="990" y="705" text-anchor="middle">保护人类共同家园</text>
        </g>

        <g class="node level2-node" @click="selectNode('global-2')">
          <rect x="850" y="780" width="280" height="80" rx="15" />
          <text x="990" y="815" text-anchor="middle">共建清洁美丽世界</text>
        </g>

        <g class="node level2-node" @click="selectNode('global-3')">
          <rect x="850" y="890" width="350" height="80" rx="15" />
          <text x="1025" y="925" text-anchor="middle">积极推动全球可持续发展</text>
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
          content: '生态文明建设是关系中华民族永续发展的根本大计，是实现中华民族伟大复兴的重要战略任务。党的十八大以来，以习近平同志为核心的党中央把生态文明建设作为统筹推进"五位一体"总体布局和协调推进"四个全面"战略布局的重要内容，开展了一系列根本性、开创性、长远性工作。我们要牢固树立社会主义生态文明观，推动形成人与自然和谐发展现代化建设新格局，坚定不移走生产发展、生活富裕、生态良好的文明发展道路。'
        },
        'harmony': {
          title: '坚持人与自然和谐共生',
          content: '人与自然是生命共同体，人类必须尊重自然、顺应自然、保护自然。大自然是人类赖以生存发展的基本条件，是生命之母。人类对大自然的伤害最终会伤及人类自身，这是无法抗拒的规律。必须站在中华民族永续发展的高度，坚持绿水青山就是金山银山的理念，推进生态文明建设和生态环境保护，建设人与自然和谐共生的现代化。'
        },
        'harmony-1': {
          title: '生态兴则文明兴',
          content: '生态环境是人类生存最为基础的条件，生态环境变化直接影响文明兴衰演替。古代埃及、古代巴比伦、古代印度、古代中国四大文明古国均发源于森林茂密、水量丰沛、田野肥沃的地区，而生态环境衰退特别是严重的土地荒漠化则导致古代埃及、古代巴比伦衰落。我国古代的河西走廊、黄土高原都曾经水丰草茂，由于毁林开荒、乱砍滥伐，致使生态环境遭到严重破坏。历史表明，生态兴则文明兴，生态衰则文明衰，人类文明的发展离不开良好生态环境这个根本基础。'
        },
        'harmony-2': {
          title: '绿水青山就是金山银山',
          content: '2005年8月15日，习近平同志在浙江安吉县余村首次提出"绿水青山就是金山银山"的科学论断。这一重要理念深刻揭示了经济发展与生态环境保护的辩证统一关系。我们既要绿水青山，也要金山银山。宁要绿水青山，不要金山银山，而且绿水青山就是金山银山。保护生态环境就是保护生产力，改善生态环境就是发展生产力。良好的生态环境蕴含着无穷的经济价值，能够源源不断创造综合效益，实现经济社会可持续发展。'
        },
        'harmony-3': {
          title: '把生态文明建设摆在全局工作的突出位置',
          content: '良好的生态环境是最公平的公共产品，是最普惠的民生福祉。生态文明建设是重大经济问题，也是关系党的使命宗旨的重大政治问题、关系民生福祉的重大社会问题。党的十八大以来，我们党把生态文明建设摆在全局工作的突出位置，纳入"五位一体"总体布局，把"坚持人与自然和谐共生"纳入新时代坚持和发展中国特色社会主义的基本方略，把"美丽中国"纳入社会主义现代化强国目标，把"绿色"纳入新发展理念。'
        },
        'beautiful': {
          title: '建设美丽中国',
          content: '建设美丽中国是全面建设社会主义现代化国家的重要目标，是实现中华民族伟大复兴中国梦的重要内容。党的二十大明确提出，到2035年基本实现社会主义现代化时，广泛形成绿色生产生活方式，碳排放达峰后稳中有降，生态环境根本好转，美丽中国目标基本实现。我们要坚持人与自然和谐共生，协同推进降碳、减污、扩绿、增长，以改善生态环境质量为核心，全面加强环境污染防治，建设人与自然和谐共生的现代化。'
        },
        'beautiful-1': {
          title: '加快形成绿色生产方式和生活方式',
          content: '绿色发展是新发展理念的重要内容，是发展观的一场深刻革命。我国经济社会发展已经进入加快绿色化、低碳化的高质量发展新阶段。要加快推动产业结构、能源结构、交通运输结构等调整优化，推进各类资源节约集约利用，积极稳妥推进碳达峰碳中和。要把"双碳"工作纳入生态文明建设整体布局和经济社会发展全局，深入推进能源、工业、建筑、交通等领域绿色低碳转型，形成节约适度、绿色低碳、文明健康的生活方式和消费模式。'
        },
        'beautiful-2': {
          title: '坚持山水林田湖草沙一体化保护和系统治理',
          content: '山水林田湖草沙是一个生命共同体，人的命脉在田，田的命脉在水，水的命脉在山，山的命脉在土，土的命脉在林和草。必须按照生态系统的整体性、系统性及其内在规律，统筹兼顾、整体施策、多措并举，全方位、全地域、全过程开展生态文明建设。要加快实施重要生态系统保护和修复重大工程，以国家重点生态功能区为支撑，加快推进青藏高原生态屏障区、黄河重点生态区、长江重点生态区和东北森林带、北方防沙带、南方丘陵山地带、海岸带等"三区四带"生态屏障建设。'
        },
        'beautiful-3': {
          title: '用最严格制度最严密法治保护生态环境',
          content: '保护生态环境必须依靠制度、依靠法治。只有实行最严格的制度、最严密的法治，才能为生态文明建设提供可靠保障。要健全源头预防、过程控制、损害赔偿、责任追究的生态环境保护体系，完善绿色生产和消费的法律制度和政策导向。要建立生态文明建设目标评价考核制度，开展领导干部自然资源资产离任审计，实行生态环境损害责任终身追究制。对破坏生态环境的行为，必须追究到底，决不能让制度成为纸老虎、稻草人。'
        },
        'global': {
          title: '共谋全球生态文明建设之路',
          content: '地球是全人类赖以生存的唯一家园，珍爱和呵护地球是人类的唯一选择。建设绿色家园是人类的共同梦想。国际社会应该携手同行，共谋全球生态文明建设之路，牢固树立尊重自然、顺应自然、保护自然的意识，坚持走绿色、低碳、循环、可持续发展之路。中国致力于推动共建地球生命共同体，积极参与全球环境治理，是全球生态文明建设的重要参与者、贡献者、引领者。我们要同筑生态文明之基，同走绿色发展之路，共同构建人类命运共同体。'
        },
        'global-1': {
          title: '保护人类共同家园',
          content: '地球是人类唯一的家园，保护生态环境、应对气候变化需要世界各国同舟共济、共同努力。面对生态环境挑战，人类是一荣俱荣、一损俱损的命运共同体，任何一国想单打独斗都无法解决。保持良好生态环境是各国人民的共同心愿和共同责任。要秉持地球生命共同体理念，开展全球行动、全球应对、全球合作，追求人与自然和谐、追求绿色发展繁荣，扎实推动全球生态文明之路行稳致远。中国将继续承担应尽的国际义务，携手共建生态良好的地球美好家园。'
        },
        'global-2': {
          title: '共建清洁美丽世界',
          content: '建设人与自然和谐共生的地球家园，要顺应世界各国人民对美好生态环境的需要，以绿色转型为驱动，坚持多边主义，推动全球环境治理体系更加公平合理。要坚持以人为本，坚持科学治理，坚持多边主义，坚持共同但有区别的责任原则。让我们携起手来，共同呵护好地球家园，推动建设持久和平、普遍安全、共同繁荣、开放包容、清洁美丽的世界，让子孙后代既能享有丰富的物质财富，又能遥望星空、看见青山、闻到花香。'
        },
        'global-3': {
          title: '积极推动全球可持续发展',
          content: '中国作为世界上最大的发展中国家，深度参与全球气候治理，同世界各国共同推进全球生物多样性治理，积极共建绿色"一带一路"，承担大国责任，展现大国担当。中国将力争2030年前实现碳达峰、2060年前实现碳中和，这是中国基于推动构建人类命运共同体的责任担当和实现可持续发展的内在要求作出的重大战略决策。我们要秉持人类命运共同体理念，推动各方全面有效实施《巴黎协定》，共同构建人与自然生命共同体，把一个清洁美丽的世界留给子孙后代。'
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
