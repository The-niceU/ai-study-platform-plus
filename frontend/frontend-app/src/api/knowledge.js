import request from './auth'

export const getKnowledgeListApi = () => {
  return request.get('/knowledge/', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
}

export const generateKnowledgeApi = (documentId) => {
  return request.post(`/knowledge/generate/${documentId}`, null, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
}

export const searchKnowledgeApi = (data) => {
  return request.post('/knowledge/search', data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
}