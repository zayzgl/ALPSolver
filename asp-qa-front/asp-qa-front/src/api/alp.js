import request from '@/utils/request'
export function solve(data) {
  return request({
    url: '/backend/solve',
    method: 'post',
    data
  })
}

export function getCase() {
  return request({
    url: '/backend/getcase',
    method: 'get'
  })
}
