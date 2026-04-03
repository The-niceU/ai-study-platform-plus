<template>
  <AppLayout>
    <div class="kb-page">
      <el-card class="main-card page-card">
        <template #header>
          <div class="header">
            <div>
              <h2 class="page-title">知识库</h2>
              <p class="page-subtitle">查看从课程资料中提取出的知识点</p>
            </div>
            <el-button type="primary" plain @click="$router.push('/')">返回首页</el-button>
          </div>
        </template>

        <div class="toolbar">
          <el-input
            v-model="documentIdInput"
            placeholder="输入 document_id 后生成知识点"
            style="width: 240px"
          />
          <el-button type="primary" @click="handleGenerate">
            生成知识点
          </el-button>
          <el-button @click="loadKnowledgeItems">
            刷新列表
          </el-button>
        </div>

        <el-divider />

        <div class="filter-bar">
        <el-input
            v-model="knowledgeSearchInput"
            placeholder="输入关键词进行知识库检索"
            clearable
            style="width: 280px"
        />
        <el-button type="primary" @click="handleKnowledgeSearch">
            检索知识库
        </el-button>

        <el-input
            v-model="searchKeyword"
            placeholder="按标题或摘要本地筛选"
            clearable
            style="width: 240px"
        />
        <el-select
            v-model="selectedTopic"
            placeholder="按主题筛选"
            clearable
            style="width: 220px"
        >
            <el-option
            v-for="topic in topicOptions"
            :key="topic"
            :label="topic"
            :value="topic"
            />
        </el-select>
        </div>

        <div class="path-box">
  <div class="path-box-left">
    <div class="path-box-title">从知识库生成学习路径</div>
    <div class="path-box-desc">
      输入一个主题，例如 graph、linear algebra、rag，系统将结合知识点生成学习路径。
    </div>
  </div>

  <div class="path-box-right">
    <el-input
      v-model="learningTopicInput"
      placeholder="输入主题，例如：graph"
      style="width: 240px"
    />
    <el-button type="success" @click="goLearningPath">
      去生成学习路径
    </el-button>
  </div>
</div>

        <div class="table-header">
          <div class="table-title">知识点列表</div>
          <el-tag type="info">{{ filteredKnowledgeItems.length }} 条知识点</el-tag>
        </div>

        <el-empty
          v-if="filteredKnowledgeItems.length === 0"
          description="当前没有符合条件的知识点。"
        />

        <el-table
          v-else
          :data="filteredKnowledgeItems"
          class="kb-table"
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="标题" min-width="220" />
          <el-table-column prop="summary" label="摘要" min-width="320" />
          <el-table-column prop="topic" label="主题" width="180" />
          <el-table-column prop="difficulty" label="难度" width="120">
            <template #default="scope">
              <el-tag size="small">{{ scope.row.difficulty || 'basic' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="openDetail(scope.row)">
                查看详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-drawer
        v-model="drawerVisible"
        title="知识点详情"
        size="40%"
      >
        <div v-if="currentItem" class="detail-panel">
          <div class="detail-block">
            <div class="detail-label">标题</div>
            <div class="detail-value">{{ currentItem.title }}</div>
          </div>

          <div class="detail-block">
            <div class="detail-label">摘要</div>
            <div class="detail-value">{{ currentItem.summary }}</div>
          </div>

          <div class="detail-row">
            <div class="detail-block small">
              <div class="detail-label">主题</div>
              <div class="detail-value">{{ currentItem.topic || '-' }}</div>
            </div>

            <div class="detail-block small">
              <div class="detail-label">难度</div>
              <div class="detail-value">{{ currentItem.difficulty || '-' }}</div>
            </div>
          </div>

          <div class="detail-row">
            <div class="detail-block small">
              <div class="detail-label">文档 ID</div>
              <div class="detail-value">{{ currentItem.document_id }}</div>
            </div>

            <div class="detail-block small">
              <div class="detail-label">Chunk ID</div>
              <div class="detail-value">{{ currentItem.chunk_id }}</div>
            </div>
          </div>

          <div class="detail-block">
            <div class="detail-label">创建时间</div>
            <div class="detail-value">{{ formatTime(currentItem.created_at) }}</div>
          </div>
        </div>
      </el-drawer>
    </div>
  </AppLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '../components/AppLayout.vue'
import { getKnowledgeListApi, generateKnowledgeApi, searchKnowledgeApi } from '../api/knowledge'

const knowledgeItems = ref([])
const documentIdInput = ref('')
const knowledgeSearchInput = ref('')
const searchKeyword = ref('')
const selectedTopic = ref('')
const drawerVisible = ref(false)
const currentItem = ref(null)
const learningTopicInput = ref('')

const loadKnowledgeItems = async () => {
  try {
    const res = await getKnowledgeListApi()
    knowledgeItems.value = res.data
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '获取知识点列表失败')
  }
}

const handleGenerate = async () => {
  if (!documentIdInput.value.trim()) {
    ElMessage.warning('请输入 document_id')
    return
  }

  try {
    const docId = Number(documentIdInput.value)
    if (!docId) {
      ElMessage.warning('document_id 必须是数字')
      return
    }

    const res = await generateKnowledgeApi(docId)
    ElMessage.success(res.data.message || '知识点生成成功')
    loadKnowledgeItems()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '生成知识点失败')
  }
}

const topicOptions = computed(() => {
  const topics = knowledgeItems.value
    .map(item => item.topic)
    .filter(Boolean)
  return [...new Set(topics)]
})

const filteredKnowledgeItems = computed(() => {
  return knowledgeItems.value.filter(item => {
    const keyword = searchKeyword.value.trim().toLowerCase()
    const matchKeyword =
      !keyword ||
      item.title.toLowerCase().includes(keyword) ||
      item.summary.toLowerCase().includes(keyword)

    const matchTopic =
      !selectedTopic.value || item.topic === selectedTopic.value

    return matchKeyword && matchTopic
  })
})

const openDetail = (item) => {
  currentItem.value = item
  drawerVisible.value = true
}

const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  if (Number.isNaN(date.getTime())) return timeStr

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')
  const second = String(date.getSeconds()).padStart(2, '0')

  return `${year}-${month}-${day} ${hour}:${minute}:${second}`
}

const handleKnowledgeSearch = async () => {
  if (!knowledgeSearchInput.value.trim()) {
    loadKnowledgeItems()
    return
  }

  try {
    const res = await searchKnowledgeApi({
      query: knowledgeSearchInput.value,
    })
    knowledgeItems.value = res.data
    ElMessage.success('知识库检索成功')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '知识库检索失败')
  }
}

const goLearningPath = () => {
  if (!learningTopicInput.value.trim()) {
    ElMessage.warning('请输入主题后再跳转')
    return
  }

  localStorage.setItem('learning_path_topic', learningTopicInput.value.trim())
  window.location.href = '/learning-path'
}

onMounted(() => {
  loadKnowledgeItems()
})
</script>

<style scoped>
.kb-page {
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

.toolbar,
.filter-bar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-bar {
  margin-bottom: 18px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.table-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2329;
}

.kb-table :deep(.el-table__cell) {
  padding-top: 14px;
  padding-bottom: 14px;
}

.detail-panel {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.detail-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.detail-block {
  padding: 16px;
  border-radius: 16px;
  background: #f7faff;
  border: 1px solid #edf2ff;
}

.detail-block.small {
  flex: 1;
  min-width: 180px;
}

.detail-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}

.detail-value {
  color: #303133;
  line-height: 1.8;
  word-break: break-word;
}

.path-box {
  margin-bottom: 18px;
  padding: 18px 20px;
  border-radius: 18px;
  background: #f7faff;
  border: 1px solid #edf2ff;
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.path-box-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2329;
  margin-bottom: 6px;
}

.path-box-desc {
  color: #606266;
  line-height: 1.8;
  font-size: 14px;
}

.path-box-right {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

</style>