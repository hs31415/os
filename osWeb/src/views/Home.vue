<script>
import router from '../router';
</script>

<template>
  <div class="content">
    <RouterLink to="/dynamic" class="dynamic">
      <div>动态分区</div>
    </RouterLink>
    <RouterLink to="/clock" class="clock">
      <div>clock算法</div>
    </RouterLink>
  </div>
  
</template>

<style scoped>

.content{
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0; 
}

.dynamic{
  padding: 10px;
}
.clock{
  padding: 10px;
}
</style>
