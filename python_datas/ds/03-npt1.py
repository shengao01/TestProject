import numpy as np

us_data = './youtube_video_data/'
uk_data = './youtube_video_data/'

us_data = np.loadtxt(us_data,delimiter=',',dtype=int)
uk_data = np.loadtxt(uk_data,delimiter=',',dtype=int)

# 添加国家信息
# 构造全为零的数据
zero_data = np.zeros()