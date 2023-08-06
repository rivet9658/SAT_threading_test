import threading
import time
from datetime import datetime
import random


class MeatFactory:
    def __init__(self):
        self.mutex = threading.Lock()  # 互斥鎖
        self.meat_inventory = {'牛肉': 10, '豬肉': 7, '雞肉': 5}  # 剩餘肉品庫存

    # 取得當前時間
    def get_datetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 取肉動作
    def get_meat(self, worker_name):
        while True:
            # 隨機取肉(隨機類型)
            meat_type_list = list(self.meat_inventory.keys())
            meat_type = random.choice(meat_type_list)
            # 如果選種之類型還有肉，則取出，若沒有則重新獲取
            if self.meat_inventory[meat_type] > 0:
                self.meat_inventory[meat_type] -= 1  # 讓該肉品類型庫存減一
                print(f"{worker_name}在 {self.get_datetime()} 取得{meat_type}")  # 列印出取得肉品訊息
                break
        return meat_type

    # 處理肉動作
    def process_meat(self, worker_name, meat_type):
        processing_time = {'牛肉': 1, '豬肉': 2, '雞肉': 3}[meat_type]  # 判斷肉品類型處理時間
        time.sleep(processing_time)  # 模擬處理時間
        print(f"{worker_name}在 {self.get_datetime()} 處理完{meat_type}")  # 列印出處理完畢訊息


def worker_process_meat(worker_name, factory):
    # 當任意肉品類型還有庫存時，持續進行取肉與處理肉動作
    while any(factory.meat_inventory.values()):
        factory.mutex.acquire()  # 鎖定互斥鎖，確保當前員工取肉時，不會有其他員工取走同一塊肉
        meat_type = factory.get_meat(worker_name)  # 進行取肉動作
        factory.mutex.release()  # 取得肉品後，解鎖互斥鎖
        factory.process_meat(worker_name, meat_type)  # 進行處理肉動作


if __name__ == "__main__":
    meal_factory = MeatFactory()  # 建立肉品工廠物件

    # 建立五個工人的執行緒
    worker_thread_list = []
    for worker in ['A', 'B', 'C', 'D', 'E']:
        worker_thread = threading.Thread(target=worker_process_meat, args=(worker, meal_factory))
        worker_thread_list.append(worker_thread)
        worker_thread.start()

    # 等待所有工人執行緒結束
    for worker_thread in worker_thread_list:
        worker_thread.join()
