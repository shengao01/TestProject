from matplotlib import pyplot as plt
import random
from matplotlib import font_manager

my_font = font_manager.FontProperties(fname='C:\\WINDOWS\\Fonts\\simsun.ttc')

x = range(10, 40)

y_1 = [random.randint(1,3) for i in range(30)]
y_2 = [random.randint(1,3) for j in range(30)]

plt.figure(figsize=(20,8), dpi=80)

plt.plot(x, y_1, label='A',color="cyan")
plt.plot(x, y_2, label='B',color="grey",linestyle='--')

_xtick_labels = ["{}岁".format(i) for i in x]
plt.xticks(x,_xtick_labels,fontproperties=my_font)
plt.yticks(range(0,9))

plt.grid(alpha=0.5, linestyle=':')
plt.legend(prop=my_font,loc="upper left")

plt.show()