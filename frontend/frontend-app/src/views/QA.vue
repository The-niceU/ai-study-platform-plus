<template>
  <AppLayout>
    <div class="qa-page">
      <div class="qa-grid">
        <el-card class="main-card input-card">
          <template #header>
            <div class="panel-header">
              <div>
                <h2 class="panel-title">智能问答</h2>
                <p class="panel-subtitle">基于已上传课程资料进行检索增强问答</p>
              </div>
            </div>
          </template>

          <el-form>
            <el-form-item label="请输入问题">
              <el-input
                v-model="query"
                type="textarea"
                :rows="6"
                placeholder="例如：讲座播放的动画短片名称是什么？"
                :disabled="loading"
              />
            </el-form-item>

            <div class="example-box">
              <div class="example-title">示例问题</div>
              <div class="example-list">
                <el-button text @click="fillExample('讲座播放的动画短片名称是什么？')">
                  讲座播放的动画短片名称是什么？
                </el-button>
                <el-button text @click="fillExample('讲座动画短片的内容是什么？')">
                  讲座动画短片的内容是什么？
                </el-button>
                <el-button text @click="fillExample('讲座中提到的核心观点有哪些？')">
                  讲座中提到的核心观点有哪些？
                </el-button>
              </div>
            </div>

            <el-form-item label="返回片段数">
              <el-input-number v-model="topK" :min="1" :max="10" :disabled="loading" />
            </el-form-item>

            <el-form-item>
              <div class="action-row">
                <el-button type="primary" :loading="loading" @click="handleAsk">
                  {{ loading ? '问答中...' : '提交问题' }}
                </el-button>
                <el-button @click="handleClear" :disabled="loading">
                  清空问题
                </el-button>
                <el-button @click="handleCopyAnswer" :disabled="!answer">
                  复制答案
                </el-button>
              </div>
            </el-form-item>

            <div class="quick-links">
  <el-button text @click="$router.push('/knowledge')">
    去知识库查看知识点
  </el-button>
  <el-button text @click="$router.push('/learning-path')">
    去学习路径生成推荐
  </el-button>
</div>
            

          </el-form>
        </el-card>

        <el-card class="main-card result-card">
          <template #header>
            <div class="panel-header">
              <div>
                <h2 class="panel-title">回答结果</h2>
                <p class="panel-subtitle">系统将基于检索到的资料片段生成答案</p>
              </div>
            </div>
          </template>

          <div v-if="loading" class="loading-box">
            <el-skeleton :rows="8" animated />
          </div>

          <div v-else-if="answer">
            <el-card class="answer-box">
              <div class="answer-text">{{ answer }}</div>
            </el-card>
          </div>

          <div v-else class="empty-box">
            <el-empty description="请输入问题并提交，系统会基于已上传资料进行智能问答" />
          </div>

          <div v-if="sources.length > 0" class="sources-section">
            <div class="sources-title">引用来源</div>
            <el-collapse>
              <el-collapse-item
                v-for="(item, index) in sources"
                :key="index"
                :title="`来源 ${index + 1} | 文件=${item.file_name || '未知文件'} | 知识点=${item.knowledge_title || '未关联'} | score=${item.score?.toFixed(4)}`"
              >
                <div class="source-card">
  <div class="source-meta">
    <div><b>文件名：</b>{{ item.file_name || '未知文件' }}</div>
    <div><b>知识点标题：</b>{{ item.knowledge_title || '未关联知识点' }}</div>
    <div><b>主题：</b>{{ item.topic || '-' }}</div>
    <div><b>难度：</b>{{ item.difficulty || '-' }}</div>
    <div><b>Chunk：</b>{{ item.chunk_index }}</div>
  </div>

  <div v-if="item.knowledge_summary" class="source-summary">
    <b>知识点摘要：</b>{{ item.knowledge_summary }}
  </div>

  <div class="source-content">
    <b>原始片段：</b>
    <div>{{ item.content }}</div>
  </div>
</div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-card>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '../components/AppLayout.vue'
import { askQuestionApi } from '../api/qa'

const query = ref('')
const topK = ref(3)
const loading = ref(false)
const answer = ref('')
const sources = ref([])

const handleAsk = async () => {
  if (!query.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }

  loading.value = true
  answer.value = ''
  sources.value = []

  try {
    const res = await askQuestionApi({
      query: query.value,
      top_k: topK.value,
    })

    answer.value = res.data.answer
    sources.value = res.data.sources || []
    ElMessage.success('问答成功')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '问答失败')
  } finally {
    loading.value = false
  }
}

const handleClear = () => {
  query.value = ''
  answer.value = ''
  sources.value = []
}

const handleCopyAnswer = async () => {
  if (!answer.value) {
    ElMessage.warning('当前没有可复制的答案')
    return
  }

  try {
    await navigator.clipboard.writeText(answer.value)
    ElMessage.success('答案已复制')
  } catch {
    ElMessage.error('复制失败')
  }
}

const fillExample = (text) => {
  query.value = text
}
</script>

<style scoped>
.qa-page {
  padding: 8px 0 24px;
}

.qa-grid {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 24px;
  align-items: start;
}

.main-card {
  border-radius: 24px;
  border: none;
  box-shadow: 0 14px 40px rgba(31, 35, 41, 0.08);
  background: linear-gradient(135deg, #ffffff 0%, #fafcff 100%);
}

.panel-title {
  margin: 0 0 8px;
  font-size: 26px;
  font-weight: 800;
  color: #1f2329;
}

.panel-subtitle {
  margin: 0;
  color: #606266;
  line-height: 1.8;
  font-size: 14px;
}

.example-box {
  margin-bottom: 18px;
  padding: 16px 18px;
  border-radius: 16px;
  background: #f7faff;
  border: 1px solid #edf2ff;
}

.example-title {
  font-size: 14px;
  font-weight: 700;
  color: #1f2329;
  margin-bottom: 10px;
}

.example-list {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
}

.action-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.answer-box {
  border-radius: 18px;
  border: none;
  background: #f8fafc;
  box-shadow: none;
}

.answer-text {
  white-space: pre-wrap;
  line-height: 1.9;
  font-size: 15px;
  color: #303133;
}

.sources-section {
  margin-top: 24px;
}

.sources-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2329;
  margin-bottom: 14px;
}

.source-content {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #303133;
}

.loading-box,
.empty-box {
  margin-top: 8px;
}

.source-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.source-meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(180px, 1fr));
  gap: 10px 16px;
  padding: 14px 16px;
  border-radius: 14px;
  background: #f7faff;
  border: 1px solid #edf2ff;
  font-size: 14px;
  color: #303133;
}

.source-summary {
  padding: 14px 16px;
  border-radius: 14px;
  background: #fcfcfd;
  border: 1px solid #f0f2f5;
  line-height: 1.8;
  color: #303133;
}

.source-content {
  padding: 14px 16px;
  border-radius: 14px;
  background: #ffffff;
  border: 1px solid #ebeef5;
  line-height: 1.8;
  color: #303133;
}

.quick-links {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: -6px;
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .source-meta {
    grid-template-columns: 1fr;
  }
}

</style>