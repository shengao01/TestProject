# coding:utf-8

from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)    # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)   # 记录的更新时间


class U_User(BaseModel, db.Model):
    """用户表"""
    __tablename__ = "u_user"

    id = db.Column(db.Integer, primary_key= True)
    user_alias_id = db.Column(db.String(255),unique=True, nullable=False) # 用户编号
    user_icon = db.Column(db.String(512))   # 头像
    user_gender = db.Column(db.Integer, default= 0)
    user_parent = db.Column(db.String(255))   # 推荐人编号
    user_agent = db.Column(db.String(255))   # 代理商编号
    user_name = db.Column(db.String(255))   # 用户名称
    user_nickname = db.Column(db.String(255))   # 用户昵称
    user_signature = db.Column(db.String(512))  # 用户签名
    user_birthday = db.Column(db.DateTime)     # 生日
    user_stature = db.Column(db.Integer, default=170)   # 身高
    user_weight = db.Column(db.Integer, default=60)
    user_coin = db.Column(db.Float(20,6), default="0.000000")    # 账户余额
    user_frozen_coin = db.Column(db.Float(20,6), default="0.000000")    # 冻结账户
    user_vurtual_coin = db.Column(db.Float(20,6), default="0.000000")    # 虚拟币余额
    user_frozen_virtual_coin = db.Column(db.Float(20,6), default="0.000000")      # 冻结虚拟币
    user_email = db.Column(db.String(255),default=None)
    user_cdate = db.Column(db.DateTime, default= datetime.now)   # 创建日期
    user_enable = db.Column(db.Boolean, default= 1)


# 后台用户角色关联表
user_role = db.Table(
    "re_agent_role",
    db.Column("User_id", db.Integer, db.ForeignKey("admin.id"), primary_key=True),
    db.Column("Role_id", db.Integer, db.ForeignKey("u_role.id"), primary_key=True)
)


# 角色权限关联表
role_perm = db.Table(
    "re_role_perm",
    db.Column("Role_id", db.Integer, db.ForeignKey("u_role.id"), primary_key=True),
    db.Column("Perm_id", db.Integer, db.ForeignKey("u_perm.id"), primary_key=True)
)


class U_Role(BaseModel, db.Model):
    """角色表"""
    __tablename__ = "u_role"

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.Integer, default= 0)   # 角色名
    role_describe = db.Column(db.Text)   # 角色描述
    role_enable = db.Column(db.Boolean, default=0)   # 是否激活
    role_perm_id = db.Column(db.Text)    # 授权字段ID集
    role_type = db.Column(db.String(64))    # 所属分类


class U_Perm(BaseModel, db.Model):
    """资源权限表"""
    __tablename__ = "u_perm"

    id = db.Column(db.Integer, primary_key=True)
    perm_parent_id = db.Column(db.Integer)      # 父资源id
    perm_name = db.Column(db.String(64), nullable=False)     # 资源权限名称
    perm_type = db.Column(db.String(64), nullable=False)        # 资源权限类型
    perm_url = db.Column(db.String(255))        # 资源URL内容
    perm_grade = db.Column(db.Integer)      #  所属层次
    perm_enable = db.Column(db.Boolean, default=0)      # 是否激活
    perm_hidden = db.Column(db.Boolean, default=0)      # 是否隐藏
    perm_child_id = db.Column(db.String(1024))      #从属与权限ID


class U_Admin(BaseModel, db.Model):
    """管理后台用户表"""
    __tablename__ = "u_admin"

    id = db.Column(db.Integer, primary_key=True)
    user_alias_id = db.Column(db.String(255), unique=True, nullable=False)  # 用户编号
    user_password_hash = db.Column(db.String(128), nullable=False)   #   密码
    user_name = db.Column(db.String(255))   # 用户名称
    user_creator = db.Column(db.String(255))  # 创建者
    user_new_login = db.Column(db.DateTime, default=datetime.now)   # 最后登陆时间
    user_subordinate = db.Column(db.Text)   # 下属id集


    # 加上property装饰器后，会把函数变为属性，属性名即为函数名
    @property
    def password(self):
        """读取属性的函数行为"""
        # print(user.password)  # 读取属性时被调用
        # 函数的返回值会作为属性值
        # return "xxxx"
        raise AttributeError("这个属性只能设置，不能读取")

    # 使用这个装饰器, 对应设置属性操作
    @password.setter
    def password(self, value):
        """
        设置属性  user.passord = "xxxxx"
        :param value: 设置属性时的数据 value就是"xxxxx", 原始的明文密码
        :return:
        """
        self.user_password_hash = generate_password_hash(value)

    # def generate_password_hash(self, origin_password):
    #     """对密码进行加密"""
    #     self.password_hash = generate_password_hash(origin_password)

    def check_password(self, passwd):
        """
        检验密码的正确性
        :param passwd:  用户登录时填写的原始密码
        :return: 如果正确，返回True， 否则返回False
        """
        return check_password_hash(self.user_password_hash, passwd)


class U_Agent(BaseModel, db.Model):
    """代理商用户表"""
    __tablename__ = "u_agent"

    id = db.Column(db.Integer, primary_key=True)
    agent_alias_id = db.Column(db.String(255), unique=True, nullable=False)  # 代理商编号
    agent_name = db.Column(db.String(255))  # 代理商名称
    agent_password = db.Column(db.String(512))      # 代理商登陆密码
    agent_parent = db.Column(db.String(255), default="")    # 代理商父级
    agent_layer = db.Column(db.Integer, default=1)  # 当前层级数
    agent_cdate = db.Column(db.DateTime, default=datetime.now)  # 创建日期
    agent_state = db.Column(db.Integer, default= 0)   # 认证状态
    agent_enabe = db.Column(db.Boolean, default=1)    # 是否可用


class U_User_Auths(BaseModel, db.Model):
    """用户身份证表"""
    __tablename__ = "u_user_auths"

    id = db.Column(db.Integer, primary_key=True)
    auths_user_id = db.Column(db.Integer, nullable=False)    #  用户编号
    auths_indentity_type = db.Column(db.Integer, nullable=False) # 身份证号码
    auths_identifier = db.Column(db.String(11), nullable=False, unique=True) # 身份证1
    auths_user_password_hash = db.Column(db.String(512), default="")  # 身份证2
    auths_user_password = db.Column(db.String(512), default="")  # 身份证3
    auths_cdate = db.Column(db.DateTime, default= datetime.now)  # 创建日期


class U_User_Card(BaseModel, db.Model):
    """用户身份证表"""
    __tablename__ = "u_user_card"

    id = db.Column(db.Integer, primary_key=True)
    card_user_id = db.Column(db.Integer)    #  用户编号
    card_number = db.Column(db.String(512), default="") # 身份证号码
    card_image1 = db.Column(db.String(512), default="") # 身份证1
    card_image2 = db.Column(db.String(512), default="")  # 身份证2
    card_image3 = db.Column(db.String(512), default="")  # 身份证3
    card_ip = db.Column(db.String(50), default=None)    # 上传ip地址
    card_device = db.Column(db.String(50), default=None)   # android|ios
    card_cdate = db.Column(db.DateTime, default= datetime.now)  # 创建日期
    card_state = db.Column(db.Integer)  # 认证状态


class U_User_Features(BaseModel, db.Model):
    """用户特征"""
    __tablename__ = "u_user_features"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=None)
    user_feat_id = db.Column(db.Integer, default=None)


class U_User_Skill(BaseModel, db.Model):
    """用户技能表"""
    __tablename__ = "u_user_skill"

    id = db.Column(db.Integer, primary_key= True)
    skill_id = db.Column(db.Integer, nullable= False)
    skill_name = db.Column(db.String(20), default= None)
    skill_user_id = db.Column(db.Integer, nullable= False)
    skill_price = db.Column(db.Float(20,6), default="0.000000")
    skill_price_type = db.Column(db.Integer, default=0)
    skill_time = db.Column(db.Integer, default="0.000000")
    skill_time_type = db.Column(db.Integer, default=0)
    skill_cdate = db.Column(db.DateTime, default=datetime.now)
    skill_enable = db.Column(db.Boolean, default=1)


class U_User_Enliven(BaseModel, db.Model):
    """用户活跃度表"""
    __tablename__ = "u_user_enliven"

    id = db.Column(db.Integer, primary_key= True)
    enliven_skill_id = db.Column(db.Integer, nullable=False)
    enliven_user_id = db.Column(db.Integer, nullable=False)
    enliven_year = db.Column(db.Integer, default=0)
    enliven_month = db.Column(db.Integer, default=0)
    enliven_day = db.Column(db.Integer, default=0)
    enliven_count = db.Column(db.Integer, default="0.000000")


class U_User_Backlist(BaseModel, db.Model):
    """黑名单"""
    __tablename__ = "u_user_backlist"

    id = db.Column(db.Integer, primary_key=True)
    back_user_id = db.Column(db.Integer, nullable=False)
    back_back_user_id = db.Column(db.Integer, nullable=False)
    back_cdate = db.Column(db.DateTime, default=datetime.now)


class U_User_Exposelist(BaseModel, db.Model):
    """举报表"""

    __tablename__ = "u_user_exposelist"

    id = db.Column(db.Integer, primary_key=True)
    expose_user_id = db.Column(db.Integer, nullable=False)
    expose_expose_user_id = db.Column(db.Integer, nullable=False)
    expose_comment = db.Column(db.String(255), default=None)
    expose_image = db.Column(db.String(50), default=None)
    expose_state = db.Column(db.Boolean, default=0)
    expose_cdate = db.Column(db.DateTime, default=datetime.now)
    expose_isdelete = db.Column(db.Boolean, default=1)


class U_Video(BaseModel, db.Model):
    """视频表"""

    __tablename__ = "u_video"

    id = db.Column(db.Integer, primary_key=True)
    video_user_id = db.Column(db.Integer, nullable=False)
    video_music_id = db.Column(db.Integer, default=0)
    video_identifying = db.Column(db.String(255), unique=True)
    video_path = db.Column(db.String(512), default=None)
    video_web = db.Column(db.String(512), default=None)
    video_name = db.Column(db.String(50), default=0)
    video_detail = db.Column(db.String(512), default=0)
    video_type = db.Column(db.Integer, default=1)
    video_cdate = db.Column(db.DateTime, default=datetime.now)
    video_enable = db.Column(db.Boolean, default=1)


class U_Video_Call(BaseModel, db.Model):
    """点赞视频表"""
    __tablename__ = "u_video_call"

    id = db.Column(db.Integer, primary_key=True)
    call_video_id = db.Column(db.Integer, nullable=False)
    call_user_id = db.Column(db.Integer, nullable=False)
    call_cdate = db.Column(db.DateTime, default=datetime.now)


class U_Video_Hate(BaseModel, db.Model):
    """踩视频表"""
    __tablename__ = "u_video_hate"

    id = db.Column(db.Integer, primary_key=True)
    hate_video_id = db.Column(db.Integer, nullable=False)
    hate_user_id = db.Column(db.Integer, nullable=False)
    hate_cdate = db.Column(db.DateTime, default=datetime.now)


class U_Video_Exposelist(BaseModel, db.Model):
    """视频举报表"""
    __tablename__ = "u_video_exposelist"

    id = db.Column(db.Integer, primary_key=True)
    expose_user_id = db.Column(db.Integer, nullable=False)
    expose_video_id = db.Column(db.Integer, nullable=False)
    expose_reason = db.Column(db.String(255), default=None)
    expose_expose_id = db.Column(db.String(255), default=None)
    expose_comment = db.Column(db.String(255), default=None)
    expose_image = db.Column(db.String(50), default=None)
    expose_state= db.Column(db.Boolean, default=0)
    expose_cdate = db.Column(db.DateTime, default=datetime.now)


class U_User_Attention(BaseModel, db.Model):
    """关注人"""
    __tablename__ = "u_user_attention"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    attention_user_id = db.Column(db.Integer, nullable=False)
    attention_cdate = db.Column(db.DateTime, default=datetime.now)


class U_Video_Shared(BaseModel, db.Model):
    """分享视频"""
    __tablename__ = "u_video_shared"

    id = db.Column(db.Integer, primary_key=True)
    shared_video_id = db.Column(db.Integer, nullable=False)
    shared_user_id = db.Column(db.Integer, nullable=False)
    shared_receipt = db.Column(db.Boolean, default=0)
    shared_cdate = db.Column(db.DateTime, default=datetime.now)


class U_Expose(BaseModel, db.Model):
    """举报理由"""
    __tablename__ = "u_expose"

    id = db.Column(db.Integer, primary_key=True)
    expose_user_id = db.Column(db.Integer, nullable=False)
    expose_state = db.Column(db.Boolean, default=0)
    expose_type = db.Column(db.Boolean, default=0)
    shared_cdate = db.Column(db.DateTime, default=datetime.now)


class U_Organization(BaseModel, db.Model):
    """用户活动"""
    __tablename__ = "u_organization"

    id = db.Column(db.Integer, primary_key=True)
    organ_alias_id = db.Column(db.Integer, nullable=False, unique=True)
    organ_skill_id = db.Column(db.Integer, nullable=False)
    organ_video_id = db.Column(db.Integer, default=None)
    organ_do_name = db.Column(db.String(512), default=None)
    organ_do_time = db.Column(db.DateTime, default=datetime.now)
    organ_do_address = db.Column(db.String(512), nullable=False)
    organ_do_people_max = db.Column(db.Integer, default=10)
    organ_do_people_min = db.Column(db.Integer, default=1)
    organ_do_lon = db.Column(db.Float(9,6), default=None)
    organ_do_lat = db.Column(db.Float(8,6), default=None)
    organ_do_city = db.Column(db.String(255), default=None)
    organ_do_detail = db.Column(db.String(255), default=None)
    organ_do_price = db.Column(db.Float(20,6), default=0.00)
    organ_do_price_unit = db.Column(db.Integer, default=1)
    organ_do_require_gender = db.Column(db.Integer, default=3)
    organ_do_require_anonymous = db.Column(db.Boolean, default=0)
    organ_cdate = db.Column(db.DateTime, default=datetime.now)
    organ_state = db.Column(db.Integer, default=0)


class U_Organization_User(BaseModel, db.Model):
    """报名人"""

    __tablename__ = "u_organization_user"

    id = db.Column(db.Integer, primary_key=True)
    organuser_organ_id = db.Column(db.Integer, nullable=False)
    organuser_user_id = db.Column(db.Integer, nullable=False)
    organuser_price = db.Column(db.Float(20,6), default=0.0)
    organuser_type = db.Column(db.Boolean, default=1)
    organuser_state = db.Column(db.Integer, default=0)
    organuser_grab_state = db.Column(db.Integer, default=0)


class O_Order(BaseModel, db.Model):
    """用户订单"""
    __tablename__ = "0_order"

    id = db.Column(db.Integer, primary_key=True)
    order_alias_id = db.Column(db.String(255), default=None)
    order_skill_id = db.Column(db.Integer, default=None)
    order_organ_id = db.Column(db.Integer, default=None)
    order_present_id = db.Column(db.Integer, default=None)
    order_do_name = db.Column(db.String(512), default=None)
    order_do_time = db.Column(db.DateTime, default=datetime.now)
    order_do_time_length = db.Column(db.Integer, default=10, nullable=True)
    order_do_time_unit = db.Column(db.Integer, nullable=False)
    order_do_address = db.Column(db.String(512), default=None)
    order_do_lon = db.Column(db.Float(9, 6), default=0)
    order_do_lat= db.Column(db.Float(8, 6), default=0)
    order_do_city = db.Column(db.String(255), default=None)
    order_do_detail = db.Column(db.String(255), default=None)
    order_do_price = db.Column(db.Float(20, 6), default=0)
    order_do_require_gender = db.Column(db.Integer, default=3)
    order_do_require_anonymous = db.Column(db.Boolean, default=0)
    order_type = db.Column(db.Integer, default=1)
    order_cdate = db.Column(db.DateTime, default=datetime.now)
    order_state = db.Column(db.Integer, default=0)


class O_Order_User(BaseModel, db.Model):
    """订单人"""
    __tablename__ = "o_order_user"

    id = db.Column(db.Integer, primary_key=True)
    orderuser_order_id = db.Column(db.Integer, nullable=False)
    orderuser_user_id = db.Column(db.Integer, nullable=False)
    orderuser_price = db.Column(db.Float(20,6), default=0)
    orderuser_type = db.Column(db.Integer, default=1)
    orderuser_state = db.Column(db.Integer, default=0)
    orderuser_grab_state = db.Column(db.Integer, default=0)


class O_Orderback(BaseModel, db.Model):
    """退单流程"""
    __tablename__ = "o_orderback"

    id = db.Column(db.Integer, primary_key=True)
    orderback_order_id = db.Column(db.Integer, nullable=False)
    orderback_user_id = db.Column(db.Integer, nullable=False)
    orderback_reason = db.Column(db.String(255), default=None)
    orderback_approve_user_id = db.Column(db.Integer, nullable=False)
    orderback_approve_reason = db.Column(db.Integer, default=None)
    orderback_state = db.Column(db.Integer, default=0)


class U_Pay_Trade_Coin(BaseModel, db.Model):
    """支付明细"""
    __tablename__ = "u_pay_trade_coin"

    id = db.Column(db.Integer, primary_key=True)
    trade_no = db.Column(db.String(255), nullable=False)
    trade_user_id = db.Column(db.Integer, nullable=False)
    trade_before_money = db.Column(db.Float(20,6), default=None)
    trade_after_money = db.Column(db.Float(20,6), default=None)
    trade_change_money = db.Column(db.Float(20,6), default=datetime.now)
    trade_money = db.Column(db.Float(20,6), nullable=False, default=0.000000)
    trade_type = db.Column(db.Integer, default=1)
    trade_debit = db.Column(db.Integer, default=0)
    trade_pay_type = db.Column(db.Integer, default=None)
    trade_pay_out_trade_no = db.Column(db.Integer, default=None)
    trade_pay_state = db.Column(db.Integer, default=0)
    trade_pay_state_cdate = db.Column(db.DateTime, default=datetime.now)
    trade_pay_app_state = db.Column(db.Integer, default=0)
    trade_pay_app_state_cdate = db.Column(db.DateTime, default=datetime.now)
    trade_cdate = db.Column(db.DateTime, default=datetime.now)


class U_Pay_Virtual_Coin(BaseModel, db.Model):
    """虚拟币充值"""
    __tablename__ = "u_pay_virtual_coin"

    id = db.Column(db.Integer, primary_key=True)
    trade_no = db.Column(db.String(255), nullable=False)
    trade_user_id = db.Column(db.Integer, nullable=False)
    trade_before_money = db.Column(db.Float(20, 6), default=None)
    trade_after_money = db.Column(db.Float(20, 6), default=None)
    trade_change_money = db.Column(db.Float(20, 6), default=datetime.now)
    trade_money = db.Column(db.Float(20, 6), nullable=False, default=0.000000)
    trade_type = db.Column(db.Integer, default=1)
    trade_debit = db.Column(db.Integer, default=0)
    trade_pay_type = db.Column(db.Integer, default=None)
    trade_pay_out_trade_no = db.Column(db.Integer, default=None)
    trade_pay_state = db.Column(db.Integer, default=0)
    trade_pay_state_cdate = db.Column(db.DateTime, default=datetime.now)
    trade_pay_app_state = db.Column(db.Integer, default=0)
    trade_pay_app_state_cdate = db.Column(db.DateTime, default=datetime.now)
    trade_cdate = db.Column(db.DateTime, default=datetime.now)


class L_Send_Sms(BaseModel, db.Model):
    """短信发送记录"""
    __tablename__ = "l_send_sms"

    id = db.Column(db.Integer, primary_key=True)
    sms_phone = db.Column(db.String(50), default=None)
    sms_code = db.Column(db.String(50), default=None)
    sms_ip = db.Column(db.String(50), default=None)
    sms_device = db.Column(db.String(50), default=None)
    sms_content = db.Column(db.Text)
    sms_cdate = db.Column(db.DateTime, default=datetime.now)
    sms_type = db.Column(db.Integer, default=0)


class L_User_Phone(BaseModel, db.Model):
    """修改手机号"""
    __tablename__ = "l_user_phone"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    new_phone = db.Column(db.String(255), nullable=True)
    old_phone = db.Column(db.String(255), nullable=True)
    cdate = db.Column(db.DateTime, default=datetime.now)


class L_User_Gps(BaseModel, db.Model):
    """gps信息"""
    __tablename__ = "l_user_gps"

    id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.Float(9,6), nullable=False)
    lat = db.Column(db.Float(9,6), nullable=False)
    stamp = db.Column(db.DateTime, datetime.now)
    userid = db.Column(db.String(255), default=None)
    token = db.Column(db.String(255), default=None)


class L_User_Login(BaseModel, db.Model):
    """登陆日志"""
    __tablename__ = "l_user_login"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, datetime.now)
    userid = db.Column(db.String(255), nullable=False)
    info = db.Column(db.String(255), default="")
    ip = db.Column(db.String(15), default="")


class L_Debug(BaseModel, db.Model):
    """测试日志"""
    __tablename__ = "l_debug"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, datetime.now)
    tag = db.Column(db.String(255), nullable=False)
    info = db.Column(db.String(255), default="", nullable=False)


class L_App_Err_Out(BaseModel, db.Model):
    """app运行错误信息收集"""
    __tablename__ = "l_app_err_out"

    id = db.Column(db.Integer, primary_key=True)
    err_user_id = db.Column(db.Integer, default=None)
    err_name = db.Column(db.String(50), default=None)
    err_device = db.Column(db.String(50), default=None)
    err_info = db.Column(db.Text )
    err_cdate = db.Column(db.DateTime, datetime.now)


class S_Price(BaseModel, db.Model):
    """支付和价格体系"""
    __tablename__ = "s_price"

    id = db.Column(db.Integer, primary_key=True)
    price_name = db.Column(db.String(255), default=None)
    price_detail = db.Column(db.String(255), default=None)
    price_balance = db.Column(db.Float(20, 6), default="0.000000")
    price_is_virtual = db.Column(db.Integer, default=0)
    price_balance_max = db.Column(db.Float(20, 6), default="0.000000")
    price_balance_min = db.Column(db.Float(20, 6), default="0.000000")
    price_balance_range = db.Column(db.Float(20, 6), default="0.000000")
    price_balance_polymerize = db.Column(db.String(1024), default="100.00,150.00")
    price_type = db.Column(db.Integer, default=None)


class S_Time(BaseModel, db.Model):
    """时间体系"""
    __tablename__ = "s_time"

    id = db.Column(db.Integer, primary_key=True)
    time_name = db.Column(db.String(255), default=None)
    time_detail = db.Column(db.String(255), default=None)
    time_unit = db.Column(db.Integer, default=1)
    time_single = db.Column(db.Integer, default="23")
    time_max = db.Column(db.Integer, default="23")
    time_min = db.Column(db.Integer, default="1")
    time_range = db.Column(db.Integer, default="1")
    time_polymerize = db.Column(db.String(1024), default="1,2,3")
    time_type = db.Column(db.Integer, default=0)


class S_Dictionary(BaseModel, db.Model):
    """时间体系"""
    __tablename__ = "s_dictionary"

    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(50), default=None)
    d_key = db.Column(db.Integer, default=None)
    d_value = db.Column(db.String(50), default=None)
    d_table = db.Column(db.String(50), default=None)
    d_cdate = db.Column(db.DateTime, default=datetime.now)


class S_Features(BaseModel, db.Model):
    """特征"""
    __tablename__ = "s_features"

    id = db.Column(db.Integer, primary_key=True)
    features_name = db.Column(db.String(50), nullable=False)


class S_Skill(BaseModel, db.Model):
    """技能"""
    __tablename__ = "s_skill"

    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(20), nullable=False)
    skill_icon = db.Column(db.String(255), default=None)
    skill_price_id = db.Column(db.Integer, nullable=False)
    skill_price_define = db.Column(db.Integer, default=0)
    skill_time_id = db.Column(db.Integer, nullable=False)
    skill_time_define = db.Column(db.Integer, default=0)
    skill_multiplier = db.Column(db.Integer, default=1)
    skill_people_min = db.Column(db.Integer, default=1)
    skill_people_max = db.Column(db.Integer, default=10)
    skill_gender = db.Column(db.Integer, default=1)
    skill_cdate = db.Column(db.DateTime, default=datetime.now)
    skill_order = db.Column(db.Integer, default=1000)
    skill_scene = db.Column(db.Integer, default=2)
    skill_recommend = db.Column(db.Integer, default=1)
    skill_enable = db.Column(db.Integer, default=1)


class S_Present(BaseModel, db.Model):
    """技能"""
    __tablename__ = "s_present"

    id = db.Column(db.Integer, primary_key=True)
    present_name = db.Column(db.String(20), nullable=False)
    present_icon = db.Column(db.String(255), nullable=False)
    present_price = db.Column(db.Integer, default=0)
    present_type = db.Column(db.DateTime, default=datetime.now)
    present_order = db.Column(db.Integer, default=1)
    present_enable = db.Column(db.Integer, default=1)


class S_Banner(BaseModel, db.Model):
    """广告"""
    __tablename__ = "s_banner"

    id = db.Column(db.Integer, primary_key=True)
    banner_name = db.Column(db.String(20), nullable=False)
    banner_url = db.Column(db.String(255), nullable=False)
    banner_type = db.Column(db.Integer, nullable=False, default=0)
    banner_cdate = db.Column(db.DateTime, default=datetime.now)
    banner_order = db.Column(db.Integer, default=1000)
    banner_position = db.Column(db.Integer, default=0)
    banner_enable = db.Column(db.Integer, default=1)


class S_Open_Citys(BaseModel, db.Model):
    """开放城市"""
    __tablename__ = "s_open_citys"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False)
    city_number = db.Column(db.String(50), nullable=False)
    city_cdate = db.Column(db.DateTime, default=datetime.now)
    city_order = db.Column(db.Integer, default=1000)
    city_enable = db.Column(db.Integer, default=1)


class S_Music(BaseModel, db.Model):
    """音乐"""
    __tablename__ = "s_music"

    id = db.Column(db.Integer, primary_key=True)
    music_type_id = db.Column(db.Integer, nullable=False)
    music_identifying = db.Column(db.String(255), nullable=False, unique=True)
    music_name = db.Column(db.String(255), nullable=False)
    music_author = db.Column(db.String(50), default=0)
    music_time = db.Column(db.Integer, default=0)
    music_path = db.Column(db.String(512), default=None)
    music_web = db.Column(db.String(512), default=None)
    music_copyright = db.Column(db.Integer, default=1)
    music_enable = db.Column(db.Integer, default=1)
    music_cdate = db.Column(db.DateTime, default=datetime.now)


class S_Music_Type(BaseModel, db.Model):
    """音乐分类"""
    __tablename__ = "s_music_type"

    id = db.Column(db.Integer, primary_key=True)
    music_parent = db.Column(db.Integer, nullable=False, default=1)
    music_typename = db.Column(db.String(255), nullable=False)


