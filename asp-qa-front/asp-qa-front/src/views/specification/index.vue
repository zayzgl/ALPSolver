<template>
  <div class="pdf">
    <div class="show">
      <pdf
        ref="pdf"
        :src="pdfUrl"
        :page="pageNum"
        :rotate="pageRotate"
        @password="password"
        @progress="loadedRatio = $event"
        @page-loaded="pageLoaded($event)"
        @num-pages="pageTotalNum = $event"
        @error="pdfError($event)"
        @link-clicked="page = $event"
      >
      </pdf>
    </div>

    <div class="pdf_footer">
      <div class="info">
        <div>当前页数/总页数：{{ pageNum }}/{{ pageTotalNum }}</div>
        <div>页面加载成功: {{ curPageNum }}</div>
      </div>
      <div class="operate">
        <div class="btn" @click.stop="prePage">上一页</div>
        <div class="btn" @click.stop="nextPage">下一页</div>
        <div class="btn" @click="scaleD">放大</div>
        <div class="btn" @click="scaleX">缩小</div>
        <div class="btn" @click.stop="clock">顺时针</div>
        <div class="btn" @click.stop="counterClock">逆时针</div>
        <div class="btn" @click="fileDownload()">下载</div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import pdf from "vue-pdf";
export default {
  name: "vue_pdf_preview",
  props: {
    // 当前pdf路径
    pdfUrl: {
      type: String,
      default:
        "http://127.0.0.1:8000/download/pdf/",
    },
  },
  components: {
    pdf,
  },
  data() {
    return {
      // 总页数
      pageTotalNum: 1,
      // 当前页数
      pageNum: 1,
      // 加载进度
      loadedRatio: 0,
      // 页面加载完成
      curPageNum: 0,
      // 放大系数 默认百分百
      scale: 100,
      // 旋转角度 ‘90’的倍数才有效
      pageRotate: 0,
      // 单击内部链接时触发 (目前我没有遇到使用场景)
      page: 0,
    };
  },
  watch: {},
  computed: {},
  created() {},
  mounted() {},
  methods: {
    //下载PDF
    fileDownload() {
      // 使用 fetch API 获取文件
      fetch(this.pdfUrl)
        .then(response => response.blob()) // 转换响应为 Blob
        .then(blob => {
          // 创建一个临时的 URL 指向 Blob 对象
          const blobUrl = window.URL.createObjectURL(blob);
          // 创建一个链接元素
          const link = document.createElement('a');
          link.href = blobUrl;
          link.download = 'downloaded.pdf'; // 可以指定下载的文件名
          // 触发下载
          link.click();
          // 清理：撤销创建的 Blob URL
          window.URL.revokeObjectURL(blobUrl);
        })
        .catch(error => {
          console.error('下载出错:', error);
        });
    },

    //放大
    scaleD() {
      this.scale += 5;
      this.$refs.pdf.$el.style.width = parseInt(this.scale) + "%";
    },

    //缩小
    scaleX() {
      // scale 是百分百展示 不建议缩放
      if (this.scale == 100) {
        return;
      }
      this.scale += -5;
      console.log(parseInt(this.scale) + "%");
      this.$refs.pdf.$el.style.width = parseInt(this.scale) + "%";
    },
    // 切换上一页
    prePage() {
      var p = this.pageNum;
      p = p > 1 ? p - 1 : this.pageTotalNum;
      this.pageNum = p;
    },
    // 切换下一页
    nextPage() {
      var p = this.pageNum;
      p = p < this.pageTotalNum ? p + 1 : 1;
      this.pageNum = p;
    },
    // 顺时针选中角度
    clock() {
      this.pageRotate += 90;
    },
    // 逆时针旋转角度
    counterClock() {
      this.pageRotate -= 90;
    },
    // pdf 有密码 则需要输入秘密
    password(updatePassword, reason) {
      updatePassword(prompt('password is "test"'));
      console.log("...reason...");
      console.log(reason);
      console.log("...reason...");
    },
    // 页面加载成功  当前页数
    pageLoaded(e) {
      this.$emit("current", e);
      this.curPageNum = e;
    },
    // 异常监听
    pdfError(error) {
      console.error(error);
    },
    // 获取当前页面pdf的文字信息内容
    logContent() {
      this.$refs.pdf.pdf.forEachPage(function (page) {
        return page.getTextContent().then(function (content) {
          let text = content.items.map((item) => item.str);
          let allStr = content.items.reduce(
            (initVal, item) => (initVal += item.str),
            ""
          );
          console.log(allStr); // 内容字符串
          console.log(text); // 内容数组
        });
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.pdf {
  padding: 20px;
  .show {
    overflow: auto;
    margin: auto;
    max-width: 75%;
    height: 80vh;
    // max-height: 530px;
  }
  .pdf_footer {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center; /* 垂直居中 */
    //position: sticky;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 10px 0px 0px 60px;
    background-color: rgba(255, 255, 255, 0.5);
    .info {
      margin: 10px 0 0;
      display: flex;
      flex-wrap: wrap;
      div {
        width: 200px;
      }
    }
    .operate {
      margin: 20px 0 0;
      display: flex;
      flex-wrap: wrap;
      div {
        // width: 80px;
        text-align: center;
        font-size: 15px;
      }
      .btn {
        cursor: pointer;
        margin: 5px 10px;
        width: 120px;
        border-radius: 5px;
        padding: 5px;
        color: #fff;
        background-color: #354464;
      }
    }
  }
}
</style>
