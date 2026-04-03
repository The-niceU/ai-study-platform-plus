<template>
  <AppLayout>
    <div class="lp-page">
      <el-card class="main-card page-card">
        <template #header>
          <div class="header">
            <div>
              <h2 class="page-title">学习路径推荐</h2>
              <p class="page-subtitle">根据知识库内容为你生成一个简单的学习路径</p>
            </div>
            <el-button type="primary" plain @click="$router.push('/')">返回首页</el-button>
          </div>
        </template>

        <div class="toolbar">
          <el-input
            v-model="topic"
            placeholder="输入学习主题，例如：讲座、动画、机器学习"
            style="width: 320px"
          />
          <el-button type="primary" :loading="loading" @click="handleGenerate">
            {{ loading ? '生成中...' : '生成学习路径' }}
          </el-button>
          
        </div>
        
        <div class="quick-links">
  <el-button text @click="$router.push('/knowledge')">
    去知识库查看知识点
  </el-button>
  <el-button text @click="$router.push('/qa')">
    去智能问答继续提问
  </el-button>
</div>

        <el-divider />

        <el-empty
          v-if="!pathData && !loading"
          description="请输入一个主题，系统会基于知识库生成学习路径。"
        />

        <div v-if="pathData" class="result-panel">
          <div class="result-topic">
            <el-tag type="success" size="large">主题：{{ pathData.topic }}</el-tag>
          </div>

          <div class="steps-list">
            <el-card
              v-for="step in pathData.steps"
              :key="step.step"
              class="step-card"
              shadow="hover"
            >
              <div class="step-top">
  <div class="step-index">Step {{ step.step }}</div>
  <el-tag type="success">{{ step.phase }}</el-tag>
</div>

<div class="step-title">{{ step.title }}</div>
<div class="step-desc">{{ step.description }}</div>

<div v-if="step.recommended_question" class="step-extra">
  <div class="extra-label">推荐问题</div>
  <div class="extra-value">{{ step.recommended_question }}</div>
</div>

<div v-if="step.suggested_action" class="step-extra">
  <div class="extra-label">建议操作</div>
  <div class="extra-value">{{ step.suggested_action }}</div>
</div>

<div class="step-meta" v-if="step.knowledge_item_id">
  对应知识点 ID：{{ step.knowledge_item_id }}
</div>
            </el-card>
          </div>
        </div>
      </el-card>
    </div>
  </AppLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '../components/AppLayout.vue'
import { generateLearningPathApi } from '../api/learningPath'

const topic = ref('')
const loading = ref(false)
const pathData = ref(null)

const handleGenerate = async () => {
  if (!topic.value.trim()) {
    ElMessage.warning('请输入学习主题')
    return
  }

  loading.value = true
  pathData.value = null

  try {
    const res = await generateLearningPathApi({
      topic: topic.value,
    })
    pathData.value = res.data
    ElMessage.success('学习路径生成成功')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '学习路径生成失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const savedTopic = localStorage.getItem('learning_path_topic')
  if (savedTopic) {
    topic.value = savedTopic
    localStorage.removeItem('learning_path_topic')
  }
})
</script>

<style scoped>
.lp-page {
  padding: 8px 0 24px;
}

.main-card {
  border-radius: 24px;
  border: none;
  box-shadow: 0 14px 40px rgba(31, 35, 41, 0.08);
}

.page-card {
  background: linear-gradient(135deg, #ffffff 0%, #fafcff 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  flex-wrap: wrap;
}

.page-title {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 800;
  color: #1f2329;
}

.page-subtitle {
  margin: 0;
  color: #606266;
  line-height: 1.8;
}

.toolbar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.result-panel {
  margin-top: 8px;
}

.result-topic {
  margin-bottom: 18px;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-card {
  border-radius: 18px;
  border: none;
  box-shadow: 0 10px 28px rgba(31, 35, 41, 0.06);
}

.step-index {
  font-size: 13px;
  color: #409eff;
  font-weight: 700;
  margin-bottom: 8px;
}

.step-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2329;
  margin-bottom: 10px;
}

.step-desc {
  color: #606266;
  line-height: 1.9;
}

.step-meta {
  margin-top: 12px;
  font-size: 13px;
  color: #909399;
}

.step-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.step-extra {
  margin-top: 14px;
  padding: 12px 14px;
  border-radius: 14px;
  background: #f7faff;
  border: 1px solid #edf2ff;
}

.extra-label {
  font-size: 13px;
  color: #409eff;
  font-weight: 700;
  margin-bottom: 6px;
}

.extra-value {
  color: #303133;
  line-height: 1.8;
}

.quick-links {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 10px;
}
</style>