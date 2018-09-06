from matplotlib import pyplot as plt
import random
# import matplotlib
from matplotlib import font_manager


# font = {'family' : 'MicroSoftYahei',
#         'weight' : 'bold',
#         'size'   : 'larger'}
#
# matplotlib.rc("font",**font)

my_font = font_manager.FontProperties(fname='C:\\WINDOWS\\Fonts\\simsun.ttc')
# my_font = font_manager.FontProperties(fname='C:\\WINDOWS\\Fonts\\Microsoft.ttc')

x = range(0, 120)
# y = [45,45,54,84,25,14,54,45,15,78,54,25]
y = [random.randint(20,35) for i in range(120)]
plt.figure(figsize=(20,8),dpi=80)
plt.plot(x, y)
# plt.savefig('./pag.png')

# 调整x轴刻度
_xtick_lables = ['10点{}分'.format(i) for i in range(60)]
_xtick_lables += ['11点{}分'.format(i) for i in range(60)]
plt.xticks(list(x)[::3],_xtick_lables[::3],rotation = 45, fontproperties=my_font)
# plt.xticks(x,_xtick_lables[::3],rotation = 45, fontproperties=my_font)

# add description
plt.xlabel('time')
plt.ylabel('temperature')
plt.title('10-12 the temperature change line')

plt.show()
# a = random.randint(1,2)
# print(a)