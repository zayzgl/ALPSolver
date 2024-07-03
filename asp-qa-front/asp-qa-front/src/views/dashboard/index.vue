<template>
  <div class="dashboard-container">
    <div class="title"><p>假设逻辑编程在线求解器</p></div>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <div class="settings">
          <div class="settings-left">
            <div class="configuration">
              <p>推理模式:</p>
              <template>
                <el-select v-model="reasoningMode" placeholder="请选择">
                  <el-option
                    v-for="item in reasoningOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </template>
            </div>
            <div class="configuration2">
              <p>模式依据:</p>
              <template>
                <el-select v-model="modeReference" placeholder="请选择">
                  <el-option
                    v-for="item in modeReferenceOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </template>
            </div>
            
            <div class="examples">
              <p>例子:</p>
              <el-select v-model="exampleValue" placeholder="请选择">
                <el-option-group
                  v-for="group in exampleOptions"
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
            </div>
          </div>
          <div class="settings-right">
            <el-button type="primary" @click="solve" icon="el-icon-video-play">启动</el-button>
          </div>
        </div>
      </div>
      <div>
        <template>
          <codemirror
            ref="newCm"
            v-model="code"
            @resize="onResize"
            :options="cmOptions"
          >
          </codemirror>
        </template>
      </div>
      <el-divider></el-divider>
      <div class="result">
        {{ prompt }}
      </div>
    </el-card>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { solve } from '@/api/alp'
import 'codemirror/mode/alp/python.js'
// 主题css
import 'codemirror/theme/neat.css'
// require active-line.js
import 'codemirror/addon/selection/active-line.js'
// closebrackets
import 'codemirror/addon/edit/closebrackets.js'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  data() {
    return {
      exampleOptions: [{
        label: '简单样例',
        options: [{
          value: 'Sick Birds',
          label: 'Sick Birds'
        }, {
          value: 'Flying Birds',
          label: 'Flying Birds'
        }, {
          value: 'Marathon Relay',
          label: 'Marathon Relay'
        }]
      }
        // , {
        //   label: '进阶样例',
        //   options: [{
        //     value: 'Traveling Salesperson',
        //     label: 'Traveling Salesperson'
        //   }, {
        //     value: 'Blocksworld Planning',
        //     label: 'Blocksworld Planning'
        //   }, {
        //     value: 'Pigeonator Propagator',
        //     label: 'Pigeonator Propagator'
        //   }]
        // }
      ],
      exampleValue: '',
      reasoningOptions: [{
        value: 'default',
        label: '默认'
      }, {
        value: 'brave',
        label: '勇敢'
      }, {
        value: 'cautious',
        label: '谨慎'
      }, {
        value: 'enumerate all',
        label: '枚举所有'
      }],
      reasoningMode: 'default',
      modeReference: 'defaultLiteral',
      modeReferenceOptions: [{
        value: 'reducedProgram',
        label: '规约程序-包含关系'
      },{
        value: 'reducedProgram',
        label: '规约程序-基数'
      },{
        value: 'reducedProgram',
        label: '默认字面量-包含关系'
      }, {
        value: 'defaultLiteral',
        label: '默认字面量-基数'
      }],
      code: '',
      prompt: '' +
        '\n初始化...' +
        '\n初始化成功',
      cmOptions: {
        tabSize: 4, // tabsize默认为4x
        styleActiveLine: true,
        lineNumbers: true, // 代码行数字
        line: true,
        mode: 'python',
        extraKeys: { 'Ctrl': 'autocomplete' },
        lineWrapping: true,
        theme: 'neat' // 主题根据需要自行配置
      }
    }
  },
  mounted() {
    // 获取 CodeMirror 组件的引用，以便后续操作
    // this.$refs.cm = this.$refs.VueCodeMirror.$refs.cmEditor.$refs.editor
    this.code = this.$route.query.code
  },
  watch: {
    exampleValue(newValue, oldValue) {
      console.log('exampleValue changed from', oldValue, 'to', newValue)
      if (newValue === 'Sick Birds') {
        this.code = '这里是Sick Birds的ALP Code'
      } else if (newValue === 'Flying Birds') {
        this.code = 'Flying Birds的ALP Code'
      } else if (newValue === 'Marathon Relay') {
        this.code = 'Marathon Relays的ALP Code'
      }
    }
  },
  methods: {
    // 子Component传递给父Component问题，
    async solve() {
      const defaultPrompt = '' + '\n初始化...' + '\n初始化成功'
      this.prompt = defaultPrompt
      const response = await this.getALPAnswer()
      const result = response.data
      this.prompt = this.prompt + '\nALP version 1.0.0\n' + '\n' + result.message
      if (result.status === 1) {
        this.prompt = this.prompt + '\n用时: ' + result.timeUsed + 's'
        this.prompt = this.prompt + '\n'
        console.log(result)
        const assumption_sets = result.assumptionSets
        for (let i = 0; i < assumption_sets.length; i++) {
          this.prompt = this.prompt + '\n' + 'Case:' + i
          this.prompt = this.prompt + '\nview number: ' + assumption_sets[i].belief_set.length
          this.prompt = this.prompt + '\n' + 'Assumption Set: ' + assumption_sets[i].assumption_set
          for (let j = 0; j < assumption_sets[i].belief_set.length; j++) {
            this.prompt = this.prompt + '\n' + 'View' + j + ':' + ' <' + assumption_sets[i].assumption_set + ',' + assumption_sets[i].belief_set[j] + '>'
          }
          this.prompt = this.prompt + '\n'
        }

      }
    },
    getALPAnswer() {
      console.log('求解！')
      const params = {
        'code': this.code,
        'mode': this.reasoningMode,
        'reference': this.modeReference
      }
      return new Promise((resolve, reject) => {
        solve(params).then(response => {
          resolve(response)
        }).catch(error => {
          reject(error)
          console.log(error)
        })
      })
    },
    onResize() {
      // 重新计算高度，这里只是一个示例，你可以根据实际需求进行调整
      this.$refs.newCm.codemirror.setSize(null, this.$refs.newCm.codemirror.defaultView.wrapper.clientHeight)
    }
  }
}
</script>
<style>
.el-table .warning-row {
  background: rgba(179, 214, 234, 0.56);
}

.el-table .success-row {
  background: #ffffff;
}
</style>
<style lang="scss" scoped>

.dashboard-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 30px 20px 20px 70px;
}

.title {
  font-size: 30px;
}

.settings {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.settings-left {
  display: flex;
  flex-direction: row;
}

.examples {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-left: 30px;
}

.examples p {
  margin-right: 30px;
}

.configuration {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.configuration2 {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-left: 20px;
}
.configuration p {
  margin-right: 30px;
}
.configuration2 p {
  margin-right: 30px;
}
.result {
  white-space: pre-wrap;
}
</style>
