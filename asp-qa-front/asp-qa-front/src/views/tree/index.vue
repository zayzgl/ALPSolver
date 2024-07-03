<template>
  <div class="app-container">
    <el-input v-model="filterText" placeholder="Filter keyword" style="margin-bottom:30px;"/>
    <el-table
      :data="cases"
      border
      style="width: 100%"
      ref="tree"
    >
      <el-table-column
        fixed
        prop="id"
        label="序号"
        width="150"
      >
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述"
        width="fit-content"
      >
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="300"
      >
        <template slot-scope="scope">
          <div class="program">
            <el-popover
              style="padding-left: 50px"
              placement="left"
              width="500"
              height="fit-content"
              trigger="click"
            >
              <codemirror
                ref="newCm"
                v-model="code"
                @resize="onResize"
                :options="cmOptions"
              >
              </codemirror>
              <el-button slot="reference" @click="handleClick(scope.row)" type="text" size="small">查看程序</el-button>
            </el-popover>
            <el-button type="text" size="small" style="padding-right: 50px" @click="haveTry(scope.row)">试一试</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getCase } from '@/api/alp'

export default {
  async mounted() {
    this.cases = await this.getCasesData()
    this.casesBackUp = await this.getCasesData()
  },
  data() {
    return {
      code: '',
      cmOptions: {
        tabSize: 4, // tabsize默认为4
        styleActiveLine: true,
        lineNumbers: true, // 代码行数字
        line: true,
        mode: 'python',
        extraKeys: { 'Ctrl': 'autocomplete' },
        lineWrapping: true,
        theme: 'neat' // 主题根据需要自行配置
      },
      casesBackUp: null,
      cases: null,
      filterText: ''
    }
  },
  watch: {
    filterText(val) {
      if (val === '' || val == null) {
        this.cases = this.casesBackUp
      } else {
        const temp = []
        for (let i = 0; i < this.cases.length; i++) {
          if (this.cases[i].description.includes(val)) {
            temp.push(this.cases[i])
          }
        }
        this.cases = temp
      }
    }
  },

  methods: {
    async getCasesData() {
      const response = await this.getCases()
      const result = response.data
      return result
    },
    handleClick(row){
      this.code = row.code
    },
    haveTry(row){
      this.$router.push({ path: '/dashboard', query: { code: row.code }});
      this.code = row.code
    },
    onResize() {
      // 重新计算高度，这里只是一个示例，你可以根据实际需求进行调整
      this.$refs.newCm.codemirror.setSize(null, this.$refs.newCm.codemirror.defaultView.wrapper.clientHeight)
    },
    getCases() {
      return new Promise((resolve, reject) => {
        getCase().then(response => {
          resolve(response)
        }).catch(error => {
          reject(error)
          console.log(error)
        })
      })
    }
  }
}
</script>
<style lang="scss" scoped>

.filter-tree {
  margin: 10px 0px 0px 30px;
}

.program {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>

