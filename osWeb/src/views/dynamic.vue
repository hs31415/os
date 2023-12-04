<script>
import { ref } from 'vue';
import router from '../router';

export default{
  data(){
    return{
      freeNum:1,
      busyArea:1,
      freeAreas: [
        { place: { start: '', length: '' } },
      ],
      busyAreas: [
        { place: { start: '', length: '', process:'' } },
      ],
    }
  },
  methods:{
    back(){
      router.push({name: 'Home'})
    },
    printArea(){
      console.log(this.freeAreas)
      console.log(this.busyAreas)
      fetch('http://127.0.0.1:8000/allocate-partitions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ free_areas: this.freeAreas, busy_areas: this.busyAreas })
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
      router.push({name: 'show'})
    },
  },
  watch: {
    freeNum(newVal) {
      const diff = newVal - this.freeAreas.length; // 计算freeAreas数组的长度变化
      if (diff > 0) { // 如果新的长度大于旧的长度，增加元素
        for (let i = 0; i < diff; i++) {
          this.freeAreas.push({ place: { start: '', length: '' } });
        }
      } else if (diff < 0) { // 如果新的长度小于旧的长度，删除元素
        this.freeAreas.splice(newVal);
      }
    },
    busyArea(newVal) {
      const diff = newVal - this.busyAreas.length; // 计算freeAreas数组的长度变化
      if (diff > 0) { // 如果新的长度大于旧的长度，增加元素
        for (let i = 0; i < diff; i++) {
          this.busyAreas.push({ place: { start: '', length: '' } });
        }
      } else if (diff < 0) { // 如果新的长度小于旧的长度，删除元素
        this.busyAreas.splice(newVal);
      }
    },
  },
}
</script>

<template>
  <div>
    <el-button @click="back()" >返回</el-button>
    <el-button @click="printArea" style="margin-left: 100px;">确定</el-button>
  </div>
  
  <el-form>
    <el-input-number v-model="this.freeNum" style="margin: 30px;"/>
  </el-form>
  <li v-for="(item, index) in freeAreas" :key="index" class="content">
    <div style="margin-right: 100px;">第{{ index+1 }}个空闲区</div>
    <el-form :model="item.place" label-position="left" label-width="80px" ref="place">
      <el-form-item label="起始地址">
        <el-input v-model="item.place.start" clearable />
      </el-form-item>
      <el-form-item label="长度">
        <el-input v-model="item.place.length" clearable />
      </el-form-item>
    </el-form>
  </li>
  <el-form>
    <el-input-number v-model="this.busyArea" style="margin: 30px;"/>
  </el-form>
  <li v-for="(item, index) in busyAreas" :key="index" class="content">
    <div style="margin-right: 100px;">第{{ index+1 }}个占用区</div>
    <el-form :model="item.place" label-position="left" label-width="80px" ref="place">
      <el-form-item label="起始地址">
        <el-input v-model="item.place.start" clearable />
      </el-form-item>
      <el-form-item label="长度">
        <el-input v-model="item.place.length" clearable />
      </el-form-item>
      <el-form-item label="进程编号">
        <el-input v-model="item.place.process" clearable />
      </el-form-item>
    </el-form>
  </li>
</template>

<style scoped>

.content{
  display: flex;
}
</style>
