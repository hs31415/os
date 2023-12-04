<template>
  <div>
    <h2>Free List:</h2>
    <ul>
      <li v-for="item in freeList" :key="item.id">
        起始地址：{{ item.start }}
        长度：{{ item.size }}
      </li>
    </ul>

    <h2>Allocated List:</h2>
    <ul>
      <li v-for="item in allocatedList" :key="item.id">
        起始地址：{{ item.start }}
        长度：{{ item.size }}
        进程编号：{{ item.process_id }}
      </li>
    </ul>
    <el-button @click="fresh">分配分区</el-button>
    <el-form :model="this.place" label-position="left" label-width="80px" ref="place">
      <el-form-item label="起始地址">
        <el-input v-model="this.place.start" clearable />
      </el-form-item>
      <el-form-item label="长度">
        <el-input v-model="this.place.length" clearable />
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      place: { start: '', length: '' },
      freeList: [],
      allocatedList: []
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      fetch('http://127.0.0.1:8000/get-data')
        .then(response => response.json())
        .then(data => {
          console.log(data)
          this.freeList = data.free_list;
          this.allocatedList = data.allocated_list;
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
    fresh(){
      fetch('http://127.0.0.1:8000/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ place: this.place})
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
      this.fetchData();
    }
  }
};
</script>
