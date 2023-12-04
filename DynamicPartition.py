from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的跨域请求，也可以设置为特定的来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)
free_list = []
allocated_list = []

# 定义空闲分区类
class FreePartition:
    def __init__(self, start, size):
        self.start = start  # 空闲分区起始位置
        self.size = size  # 空闲分区大小


# 定义已分配分区类
class AllocatedPartition:
    def __init__(self, start, size, process_id):
        self.start = start  # 已分配分区起始位置
        self.size = size  # 已分配分区大小
        self.process_id = process_id  # 进程ID


# 定义动态分区管理类
class DynamicPartition:
    def __init__(self, free_list, allocated_list):
        self.free_list = free_list  # 空闲分区列表
        self.allocated_list = allocated_list  # 已分配分区列表

    # 最先适应算法分配内存
    def allocate_first_fit(self, process_id, size):
        for i in range(len(self.free_list)):
            if self.free_list[i].size >= size:
                allocated_partition = AllocatedPartition(self.free_list[i].start, size, process_id)
                self.allocated_list.append(allocated_partition)
                if self.free_list[i].size > size:
                    self.free_list[i].start += size
                    self.free_list[i].size -= size
                else:
                    del self.free_list[i]
                return True
        return False

    # 最佳适应算法分配内存
    def allocate_best_fit(self, process_id, size):
        best_index = -1
        for i in range(len(self.free_list)):
            if self.free_list[i].size >= size:
                if best_index == -1 or self.free_list[i].size < self.free_list[best_index].size:
                    best_index = i
        if best_index != -1:
            allocated_partition = AllocatedPartition(self.free_list[best_index].start, size, process_id)
            self.allocated_list.append(allocated_partition)
            if self.free_list[best_index].size > size:
                self.free_list[best_index].start += size
                self.free_list[best_index].size -= size
            else:
                del self.free_list[best_index]
            return True
        return False

    # 最坏适应算法分配内存
    def allocate_worst_fit(self, process_id, size):
        worst_index = -1
        for i in range(len(self.free_list)):
            if self.free_list[i].size >= size:
                if worst_index == -1 or self.free_list[i].size > self.free_list[worst_index].size:
                    worst_index = i
        if worst_index != -1:
            allocated_partition = AllocatedPartition(self.free_list[worst_index].start, size, process_id)
            self.allocated_list.append(allocated_partition)
            if self.free_list[worst_index].size > size:
                self.free_list[worst_index].start += size
                self.free_list[worst_index].size -= size
            else:
                del self.free_list[worst_index]
            return True
        return False

    # 回收内存
    def deallocate(self, process_id):
        for i in range(len(self.allocated_list)):
            if self.allocated_list[i].process_id == process_id:
                free_partition = FreePartition(self.allocated_list[i].start, self.allocated_list[i].size)
                self.free_list.append(free_partition)
                del self.allocated_list[i]
                break
        self.merge_free_partitions()

    # 合并相邻空闲分区
    def merge_free_partitions(self):
        # 先按照起始地址对分区列表进行排序
        self.free_list.sort(key=lambda partition: partition.start)

        i = 0
        while i < len(self.free_list) - 1:
            if self.free_list[i].start + self.free_list[i].size == self.free_list[i + 1].start:
                self.free_list[i].size += self.free_list[i + 1].size
                del self.free_list[i + 1]
            else:
                i += 1

    # 显示当前分区情况
    def display(self):
        print("已占用分区：")
        for partition in self.allocated_list:
            print("起始位置：{}，大小：{}，进程ID：{}".format(partition.start, partition.size, partition.process_id))
        print("空闲分区：")
        for partition in self.free_list:
            print("起始位置：{}，大小：{}".format(partition.start, partition.size))

dynamic_partition = DynamicPartition(free_list, allocated_list)

@app.post("/allocate-partitions")
def allocate_partitions(free_areas: List[dict], busy_areas: List[dict]):
    global free_list
    global allocated_list
    print(free_areas)
    print(busy_areas)
    # 根据请求中的空闲区域创建 FreePartition 对象
    for item in free_areas:
        place = item.get('place')
        if place:
            start = int(place.get('start', 0))
            length = int(place.get('length', 0))
            free_partition = FreePartition(start, length)
            free_list.append(free_partition)

    for item in busy_areas:
        place = item.get('place')
        if place:
            start = int(place.get('start', 0))
            length = int(place.get('length', 0))
            process = int(place.get('process', 0))
            allocated_partition = AllocatedPartition(start, length, process)
            allocated_list.append(allocated_partition)

    print(free_list)
    print(allocated_list)
    # 进行分配操作，返回结果
    return {"free_list": free_list, "allocated_list": allocated_list}

@app.get("/get-data")
async def get_data():
    global free_list
    global allocated_list
    return {"free_list": free_list, "allocated_list": allocated_list}

@app.post("/add")
async def add():
    global free_list
    global allocated_list
    dynamic_partition.allocate_first_fit(process_id, size)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000, proxy_headers=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
