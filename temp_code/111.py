# coding=utf-8
from pyecharts import Geo, Style


style = Style()
data=[('天津',99),('昆明',199),('秦皇岛',299)]
geo= Geo('城市', '', **style.init_style)

attr,value=geo.cast(data)
geo.add('', attr, value, type="effectScatter", is_label_show=True, label_pos='outside',
        label_formatter='{b}', is_more_utils=True, is_label_emphasis=True, label_text_color='#FFFFFF', effect_scale=5, label_text_size=9,is_visualmap=True,visual_range=[0, 300])

geo.render('aaa.gif')