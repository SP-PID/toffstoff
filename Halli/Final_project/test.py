import time
idle_time = time.time()
time.sleep(2)
current_pause = time.time() - idle_time
print(current_pause)