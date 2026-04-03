<template>
  <div class="layout">
    <header class="navbar">
      <div class="nav-left" @click="$router.push('/')">
        <div class="logo">AI</div>
        <div class="brand">
          <div class="brand-title">AI 学习平台</div>
          <div class="brand-subtitle">RAG 智能问答系统</div>
        </div>
      </div>

      <div class="nav-right">
        <el-button :type="isActive('/') ? 'primary' : ''" text @click="$router.push('/')">首页</el-button>
        <el-button :type="isActive('/documents') ? 'primary' : ''" text @click="$router.push('/documents')">文档管理</el-button>
        <el-button :type="isActive('/knowledge') ? 'primary' : ''" text @click="$router.push('/knowledge')">知识库</el-button>
        <el-button :type="isActive('/qa') ? 'primary' : ''" text @click="$router.push('/qa')">智能问答</el-button>
        <el-button :type="isActive('/learning-path') ? 'primary' : ''" text @click="$router.push('/learning-path')">学习路径</el-button>

        <el-divider direction="vertical" />

        <el-button v-if="!isLoggedIn" type="primary" plain @click="$router.push('/login')">
          登录
        </el-button>
        <el-button v-if="!isLoggedIn" @click="$router.push('/register')">
          注册
        </el-button>
        <el-button v-if="isLoggedIn" type="danger" plain @click="logout">
          退出
        </el-button>
      </div>
    </header>

    <main class="main-container">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token')
})

const logout = () => {
  localStorage.removeItem('token')
  ElMessage.success('已退出登录')
  router.push('/login')
}

const isActive = (path) => route.path === path
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(64, 158, 255, 0.08), transparent 22%),
    radial-gradient(circle at top right, rgba(124, 92, 255, 0.08), transparent 24%),
    #f6f8fb;
}

.navbar {
  height: 74px;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(235, 238, 245, 0.9);
  box-shadow: 0 6px 24px rgba(31, 35, 41, 0.04);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
}

.logo {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #409eff, #7c5cff);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 18px;
  box-shadow: 0 10px 24px rgba(64, 158, 255, 0.25);
}

.brand-title {
  font-size: 18px;
  font-weight: 700;
  color: #303133;
}

.brand-subtitle {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 20px 36px;
}

@media (max-width: 900px) {
  .navbar {
    padding: 0 16px;
    height: auto;
    min-height: 72px;
    flex-wrap: wrap;
    gap: 12px;
    padding-top: 12px;
    padding-bottom: 12px;
  }

  .nav-right {
    width: 100%;
    flex-wrap: wrap;
  }
}
</style>