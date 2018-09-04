# coding:utf-8
import itchat
import re

itchat.login() #登录微信，扫二维码
friends = itchat.get_friends(update=True)[0:] #爬取自己的好友相关信息，返回json
siglist = []
# text = ''
for i in friends:
    signature = i["Signature"].strip().replace("span","").replace("class","").replace("emoji","")
    rep = re.compile("1fd+w*|[<>/=]")
    signature = rep.sub("", signature)
    siglist.append(signature)
text = "-".join(siglist)
for sign in siglist:
    with open('sign.txt','a',encoding="gbk") as f:
        f.write(sign+'\n')


print(text)

def drawImage(word_space_split):
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, ImageColorGenerator
    import numpy as np
    import PIL.Image as Image
    coloring = np.array(Image.open("./test1.jpg"))
    my_wordcloud = WordCloud(background_color="white", max_words=2000,
    mask=coloring, max_font_size=100, random_state=42, scale=2,
    font_path="/Windows/Fonts/SimHei.ttf").generate(word_space_split)
    image_colors = ImageColorGenerator(coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()


import jieba
wordlist = jieba.cut(text, cut_all=True)
word_space_split = " ".join(wordlist)
drawImage(word_space_split)

