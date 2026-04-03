
<template>
<AppLayout>
  <div class="home-page">
    <el-card class="hero-card main-card">
      <div class="hero-top">
        <div>
          <h1 class="title">AI 学习平台</h1>
          <p class="subtitle">
            面向课程学习场景的 RAG 学习平台，支持知识库检索、引用溯源、智能问答与学习路径推荐。
          </p>
        </div>

        <div class="status-box">
          <div class="status-item">
            <span class="label">登录状态：</span>
            <el-tag :type="isLoggedIn ? 'success' : 'info'">
              {{ isLoggedIn ? '已登录' : '未登录' }}
            </el-tag>
          </div>

          <div class="status-item">
            <span class="label">后端状态：</span>
            <el-tag :type="backendStatus === 'ok' ? 'success' : 'warning'">
              {{ backendStatus }}
            </el-tag>
          </div>
        </div>
      </div>

      <div class="hero-actions">
        <el-button type="primary" @click="checkBackend">检查后端连接</el-button>
        <el-button v-if="!isLoggedIn" @click="$router.push('/login')">去登录</el-button>
        <el-button v-if="!isLoggedIn" @click="$router.push('/register')">去注册</el-button>
        <el-button v-if="isLoggedIn" type="danger" @click="logout">退出登录</el-button>
      </div>
    </el-card>

    <div class="card-grid">
      <el-card class="feature-card main-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>文档管理</span>
          </div>
        </template>

        <p class="card-desc">
          上传、查看、删除课程资料，支持 txt / docx / pdf 文档管理。
        </p>

        <el-button type="success" @click="goDocuments">
          进入文档管理
        </el-button>
      </el-card>

      <el-card class="feature-card main-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>智能问答</span>
          </div>
        </template>


        <p class="card-desc">
          基于课程资料进行检索增强问答，返回答案并展示引用来源。
        </p>

        <el-button type="warning" @click="goQA">
          进入智能问答
        </el-button>
      </el-card>

      <el-card class="feature-card main-card" shadow="hover">
  <template #header>
    <div class="card-header">
      <span>知识库</span>
    </div>
  </template>

  <p class="card-desc">
    查看从文档内容中抽取出的知识点，逐步构建面向学习场景的结构化知识库。
  </p>

  <el-button type="primary" @click="$router.push('/knowledge')">
    进入知识库
  </el-button>
    </el-card>
    
    <el-card class="feature-card main-card" shadow="hover">
  <template #header>
    <div class="card-header">
      <span>学习路径</span>
    </div>
  </template>

  <p class="card-desc">
    基于知识库内容生成主题学习路径，帮助你按顺序理解知识点并构建学习路线。
  </p>

  <el-button type="success" @click="$router.push('/learning-path')">
    进入学习路径
  </el-button>
  </el-card>

    </div>
  </div>
</AppLayout>
</template>

<script setup>
import AppLayout from '../components/AppLayout.vue'

import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const backendStatus = ref('未检查')

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token')
})

const checkBackend = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/health')
    backendStatus.value = res.data.status
    ElMessage.success('后端连接正常')
  } catch (error) {
    backendStatus.value = '连接失败'
    ElMessage.error('后端连接失败')
    console.error(error)
  }
}

const logout = () => {
  localStorage.removeItem('token')
  ElMessage.success('已退出登录')
  router.push('/login')
}

const goDocuments = () => {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  router.push('/documents')
}

const goQA = () => {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  router.push('/qa')
}

onMounted(() => {
  checkBackend()
})
</script>

<style scoped>
.home-page {
  padding: 8px 0 24px;
}

.main-card {
  border-radius: 24px;
  border: none;
  box-shadow: 0 14px 40px rgba(31, 35, 41, 0.08);
}

.hero-card {
  margin-bottom: 28px;
  background: linear-gradient(135deg, #ffffff 0%, #f7faff 100%);
}

.hero-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  flex-wrap: wrap;
}

.title {
  margin: 0 0 14px;
  font-size: 42px;
  font-weight: 800;
  color: #1f2329;
  letter-spacing: -0.5px;
}

.subtitle {
  margin: 0;
  font-size: 16px;
  color: #606266;
  line-height: 1.9;
  max-width: 760px;
}

.status-box {
  min-width: 220px;
  padding: 8px 0;
}

.status-item {
  margin-bottom: 14px;
  font-size: 14px;
}

.label {
  margin-right: 8px;
  color: #606266;
}

.hero-actions {
  margin-top: 28px;
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(280px, 1fr));
  gap: 24px;
}

.feature-card {
  min-height: 240px;
  transition: all 0.25s ease;
  background: #ffffff;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 44px rgba(31, 35, 41, 0.1);
}

.card-header {
  font-size: 20px;
  font-weight: 700;
  color: #1f2329;
}

.card-desc {
  color: #606266;
  line-height: 1.9;
  margin-bottom: 30px;
  font-size: 15px;
}

@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
  }

  .title {
    font-size: 32px;
  }
}
</style>