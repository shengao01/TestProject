# coding: utf-8
import threading
import time

def threadTest():
    start_str = "%s start time is %s" % (threading.current_thread().name, time.time())
    print(start_str)
    time_sleep = 5 + int(threading.current_thread().name[-1])  # 设置为不同的sleep时间是为了使join更容易理解
    time.sleep(time_sleep)
    end_str = "%s end time is %s" % (threading.current_thread().name, time.time())
    print(end_str)

threads = []
for i in range(3):
    t = threading.Thread(target=threadTest)
    # 此处的意思是将线程设置为守护线程,当主线程执行完毕会自动退出,设置为False则join无效,即主线程即使运行完成也会等到子线程运行完再退出
    t.setDaemon(True)
    threads.append(t)

for t in threads:
    t.start()
    # t.join()  # 此处设置阻塞将会导致线程依次执行
threads[0].join() # 设置线程阻塞,等待该子线程结束时主线程结束运行
print("finished...")
