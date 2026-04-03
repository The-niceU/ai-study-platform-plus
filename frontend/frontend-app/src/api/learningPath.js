import request from './auth'

export const generateLearningPathApi = (data) => {
  return request.post('/learning-path/', data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
}