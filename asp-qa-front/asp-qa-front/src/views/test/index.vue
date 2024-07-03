<template>
  <div class="container">
    <div class="container-top">
      <div class="container-top-left">
        <el-select v-model="queries" placeholder="请选择" multiple="true" class="container-top-left-search">
          <el-option-group
            multiple="true"
            v-for="group in options"
            :key="group.label"
            :label="group.label"
          >
            <el-option
              v-for="item in group.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-option-group>
        </el-select>
        <el-button slot="append" icon="el-icon-search" @click="handleSearch" class="container-top-left-button"
        ></el-button>
      </div>
      <div class="container-top-right">
        <el-button slot="append" icon="el-icon-delete" @click="clear" class="container-top-right-clear"></el-button>
      </div>

    </div>
    <div class="container-content">
      <div class="container-content-precise">
        <div class="container-content-precise-1">
          问答准确率:
        </div>
        <div class="container-content-precise-2">
          <el-progress :text-inside="true" :stroke-width="26" :percentage=queriesAnswer.qaScore></el-progress>
        </div>
        <div class="container-content-precise-3">
          实体链接准确率:
        </div>
        <div class="container-content-precise-4">
          <el-progress :text-inside="true" :stroke-width="24" :percentage=queriesAnswer.enScore status="success"
          ></el-progress>
        </div>
      </div>
      <div class="container-content-main">
        <div v-for="ans in queriesAnswer.answerItems" :key="ans.query" class="each_item">
          <div class="box-card-container">
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span>{{ ans.query }}</span>
              </div>
              <div class="answer">
                问题的答案是：{{ ans.answer }}
              </div>
              <div class="explanation">
                问题的解释是：{{ ans.explanation }}
              </div>
            </el-card>
          </div>
          <div class="content-right">
            <el-card class="box-card" body-style="height: 100%" shadow="always">
              <el-table
                :data="ans.NERResult"
                height="191px"
                style="width: 100%"
                :row-class-name="tableRowClassName"
              >
                <el-table-column
                  prop="mention"
                  label="指称"
                  width="80"
                >
                </el-table-column>
                <el-table-column
                  prop="entity"
                  label="实体"
                  width="80"
                >
                </el-table-column>
              </el-table>
            </el-card>
          </div>
        </div>
        <div class="space">
        </div>
      </div>
    </div>

  </div>
</template>

<script>

import { knowledge_graph_test } from '@/api/alp'

export default {
  name: 'Test',
  mounted() {

  },
  data() {
    return {
      queries: '',
      options: [
        {
          label: '1.查询某一类事物、或某一实例事物的定义',
          options: [{
            value: '航母的定义是什么？',
            label: '航母的定义是什么？'
          }, {
            value: '特种车辆的定义是什么？',
            label: '特种车辆的定义是什么？'
          },
            {
              value: '北约（北大西洋公约）的定义是什么？',
              label: '北约（北大西洋公约）的定义是什么？'
            },
            {
              value: '东盟的定义是什么？',
              label: '东盟的定义是什么？'
            },
            {
              value: '南海区域的定义是什么？',
              label: '南海区域的定义是什么？'
            },
            {
              value: '沙加地带的定义是什么？',
              label: '沙加地带的定义是什么？'
            },
            {
              value: '自由航行的定义是什么？',
              label: '自由航行的定义是什么？'
            }

          ]
        }, {
          label: '2.查询某一实例某些方面的数据类型属性值',
          options: [{
            value: '卡尔文森号的载员情况？',
            label: '卡尔文森号的载员情况？'
          }, {
            value: '卡尔文森号的最高航速？',
            label: '卡尔文森号的最高航速？'
          }, {
            value: '渥太华号护卫舰的长度是多少？',
            label: '渥太华号护卫舰的长度是多少？'
          }, {
            value: '佩拉尔塔号驱逐舰乘员数是多少？',
            label: '佩拉尔塔号驱逐舰乘员数是多少？'
          }, {
            value: '猛禽的最高航速是多少？',
            label: '猛禽的最高航速是多少？'
          },
            {
              value: '施毅的头衔是什么？',
              label: '施毅的头衔是什么？'
            },
            {
              value: '哈马斯的成立时间？',
              label: '哈马斯的成立时间？'
            }
            ,
            {
              value: '哈马斯的官方名称？',
              label: '哈马斯的官方名称？'
            }
            ,
            {
              value: '中业岛被侵占的时间是哪一年？',
              label: '中业岛被侵占的时间是哪一年？'
            },
            {
              value: '弹丸岛被侵占的时间是哪一年？',
              label: '弹丸岛被侵占的时间是哪一年？'
            }
            ,
            {
              value: '南威岛被侵占的时间是哪一年？',
              label: '南威岛被侵占的时间是哪一年？'
            }
          ]
        },

        {
          label: '4.查询某一实例事物的属性的定义',
          options: [{
            value: '航空母舰的部署地区的定义是什么',
            label: '航空母舰的部署地区的定义是什么'
          }, {
            value: '请解释航空母舰的部署地区',
            label: '请解释航空母舰的部署地区'
          }]
        }

        , {
          label: '5.查询属性值为某一给定值的一类事物',
          options: [{
            value: '制造商为莱茵金属公司的坦克有哪些？',
            label: '制造商为莱茵金属公司的坦克有哪些？'
          }, {
            value: '事件发生地点为南海地区的事件有哪些？',
            label: '事件发生地点为南海地区的事件有哪些？'
          }
            , {
              value: '事件发生地点为黄岩岛的事件有哪些？',
              label: '事件发生地点为黄岩岛的事件有哪些？'
            }
          ]
        }
        , {
          label: '6.查询某一类事物的下属分类',
          options: [{
            value: '战机有哪些类型？',
            label: '战机有哪些类型？'
          }, {
            value: '坦克有哪些类型？',
            label: '坦克有哪些类型？'
          }
            , {
              value: '事件有哪些类型？',
              label: '事件有哪些类型？'
            }

          ]
        }
        , {
          label: '10.比较两个实例的某一方面属性值哪个更大/更小',
          options: [{
            value: 'P8和F22战斗机谁的飞行速度更快？',
            label: 'P8和F22战斗机谁的飞行速度更快？'
          }, {
            value: '台风战斗机和阵风战斗机谁的乘员数更大？',
            label: '台风战斗机和阵风战斗机谁的乘员数更大？'
          }, {
            value: '歼20和F22战斗机谁的飞行速度更快？',
            label: '歼20和F22战斗机谁的飞行速度更快？'
          }
          ]
        }
        , {
          label: '11.由问题（5）和（7）组成的问题',
          options: [{
            value: '歼20出现在哪些美国的参与的军事冲突中？',
            label: '歼20出现在哪些美国的参与的军事冲突中？'
          }
            , {
              value: '054A护卫舰出现在哪些2023年的跟踪监视中？',
              label: '054A护卫舰出现在哪些2023年的跟踪监视中？'
            }

          ]
        }
        , {
          label: '12.由两个（7）类型的问题组成的问题',
          options: [{
            value: '何塞黎刹级护卫舰参与的入侵领海和佩拉尔塔号驱逐舰参与的自由航行两者时间上谁先？',
            label: '何塞黎刹级护卫舰参与的入侵领海和佩拉尔塔号驱逐舰参与的自由航行两者时间上谁先？'
          }]
        },
        {
          label: '13.对一个/类实例某方面活动的提问',
          options: [{
            value: '福特号是否参与过南海自由航行活动？',
            label: '福特号是否参与过南海自由航行活动？'
          }]
        },
        {
          label: '16.对某方面活动的属性的比较进行提问',
          options: [{
            value: '美国舰船自由航行离我岛礁最近的距离是多少？',
            label: '美国舰船自由航行离我岛礁最近的距离是多少？'
          }]
        }
        ,

        {
          label: '19.提问满足某些约束的事件之间的时序/空间等属性上的对比关联',
          options: [{
            value: '何塞黎刹级护卫舰参与的入侵领海和佩拉尔塔号驱逐舰参与的自由航行两者时间上谁先？',
            label: '何塞黎刹级护卫舰参与的入侵领海和佩拉尔塔号驱逐舰参与的自由航行两者时间上谁先？'
          }]
        }
      ],
      queriesAnswer: {
        qaScore: 0,
        enScore: 0,
        answerItems: []
      }

    }
  },
  props: {},
  methods: {
    async handleSearch() {
      const response = await this.answerRequest({ 'query': this.queries })
      this.queriesAnswer = response.data
    },
    tableRowClassName({ row }) {
      console.log(row.type)
      if (row.type === 'entity') {
        return 'success-row'
      } else {
        return 'warning-row'
      }
    },
    answerRequest(query) {
      return new Promise((resolve, reject) => {
        knowledge_graph_test(query).then(response => {
          resolve(response)
        }).catch(error => {
          reject(error)
          console.log(error)
        })
      })
    },
    clear() {
      this.queries = null
      this.queriesAnswer.enScore = 0
      this.queriesAnswer.qaScore = 0
      this.queriesAnswer.answerItems = []
    }
  }
}
</script>
<style>
.container-top {
  width: 80vw;
  height: max-content;
  margin: 30px 0px 0px 30px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.container-top-left {
  display: flex;
  flex-direction: row;
  margin: 10px 0px 0px 30px;
}

.container-top-left-search {
  width: 60vw;
  padding-top: 25px;
  padding-bottom: 25px;
}

.container-top-left-button {
  margin-top: 25px;
  margin-bottom: 25px;
}

.container-top-right {
  display: flex;
  flex-direction: row;
  margin: 10px 30px 0px 30px;
}

.container-top-right-clear {
  margin-top: 25px;
  margin-bottom: 25px;
}

.container-content {
  display: flex;
  flex-direction: column;
}

.container-content-precise {
  width: 80vw;
  height: 85px;
  margin: 30px 0px 0px 30px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: row;
}

.container-content-precise-1 {
  font-weight: bold;
  width: 8vw;
  margin: 30px 0px 0px 15px;
}

.container-content-precise-2 {
  margin: 25px 0px 0px 15px;
  height: 90px;
  width: 25vw;
}

.container-content-precise-3 {
  margin: 30px 0px 0px 20px;
  font-weight: bold;
  width: 10vw;
}

.container-content-precise-4 {
  margin: 25px 0px 0px 0px;
  height: 90px;
  width: 25vw;
}

.container-content-main {
  display: flex;
  flex-direction: column;
  height: fit-content;
  width: fit-content;
}

.box-card-container {
  width: 70vw;
  height: max-content;

}

.space {
  margin-bottom: 50px;
}

.clearfix {
  font-weight: bold;
}

.answer {
  height: 68px;
  padding-top: 10px;
}

.explanation {
  height: 68px;
  padding-top: 10px;
}

.content-right {
  display: flex;
  flex-direction: column;

}

.each_item {
  width: 80vw;
  display: flex;
  flex-direction: row;
  margin: 30px 0px 0px 30px;
}
</style>
