<template>
  <div>
    <!-- 图片点击区域 -->
    <img
      src="https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
      alt="点击显示选择列表"
      @click="showDropdown = !showDropdown"
      style="cursor: pointer; width: 100px;"/>

    <!-- 选择列表 -->
    <div v-show="showDropdown" class="dropdown-list">
      <ul>
        <li @click="selectOption('选项1')">选项1</li>
        <li @click="selectOption('选项2')">选项2</li>
        <li @click="selectOption('选项3')">选项3</li>
        <!-- 添加更多选项 -->
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false, // 控制选择列表显示的布尔值
    }
  },
  methods: {
    selectOption(option) {
      console.log('您选择了:', option);
      this.showDropdown = false; // 选择后隐藏列表
    }
  }
}
</script>

<style>
/* 选择列表的基本样式 */
.dropdown-list {
  position: absolute; /* 根据需要调整定位 */
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: white;
  width: 100%; /* 根据需要调整宽度 */
  z-index: 1000; /* 确保列表在最上面 */
}

.dropdown-list ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown-list ul li {
  padding: 8px 16px;
  cursor: pointer;
}

.dropdown-list ul li:hover {
  background-color: #f0f0f0;
}
</style>
