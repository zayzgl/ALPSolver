import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/backend/table/list',
    method: 'get',
    params
  })
}
