<template lang="html" id="layout">
  <div class="manage">
    <el-row class="top_nav">
        <el-col :span="18" :offset="3" class="header">
            <el-row>
                <el-col :span="8"  class="admin-title">
                喵约客户管理系统
                </el-col>
                <el-col :span="16" class="userinfo">
                    <div class="right_handle">
                        <span v-show="userName">欢迎您，{{userName}}</span>
                        <a href="javascript:;" @click="handleLogout" class="quit">{{userName?'退出登录':''}}</a>
                        <a href="javascript:;" @click="dialogFormVisible = true" class="quit">{{userName?'修改密码':''}}</a>
                    </div>
                </el-col>
            </el-row>
        </el-col>
    </el-row>
    <div class="mainer">
      <el-row class="tac">
        <el-col :span="3" class="side_menu">
          <el-menu
            router
            :default-active="$route.path"
            class="el-menu-vertical-demo"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b">
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-news"></i>
                <span>客户管理&nbsp;&nbsp;&nbsp;&nbsp;</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/custom_list/no_confirm">未确认客户</el-menu-item>
                <el-menu-item index="/custom_list/confirm">已确认客户</el-menu-item>
                <el-menu-item index="/custom_list/delete_user">已删除客户</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="2" v-show="level == '1'? true: false">
              <template slot="title">
                <i class="el-icon-menu"></i>
                <span>管理员管理</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/super_list">管理员列表</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
          </el-menu>
        </el-col>
        <router-view></router-view>
      </el-row>
    </div>
    <el-dialog title="修改密码" align="left" :visible.sync="dialogFormVisible" width="25%" @close="closeDialogHandle">
        <el-form :model="passInfo" status-icon :rules="rules2" ref="passInfo" >
            <el-form-item label="旧密码：" prop="oldpassword" label-width="90px">
                <el-input v-model="passInfo.oldpassword" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="新密码：" prop="password" label-width="90px">
                <el-input type="password" v-model="passInfo.password" auto-complete="off" size="medium"></el-input>
            </el-form-item>
            <el-form-item label="确认密码：" prop="user_pass2" label-width="90px">
                <el-input type="password" v-model="passInfo.password2" auto-complete="off" size="medium"></el-input>
            </el-form-item>
        </el-form>
        <div class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="subFormHandle()">确 定</el-button>
        </div>
    </el-dialog>
  </div>
</template>
<script>
    function removeCookie(key) {
        setCookie(key, '', -1);//这里只需要把Cookie保质期退回一天便可以删除
    }
    function setCookie(key, value, iDay) {
        var oDate = new Date();
        oDate.setDate(oDate.getDate() + iDay);
        document.cookie = key + '=' + value + ';expires=' + oDate;
    }
    function getCookie(key) {
        var cookieArr = document.cookie.split('; ');
        for(var i = 0; i < cookieArr.length; i++) {
          var arr = cookieArr[i].split('=');
          if(arr[0] === key) {
              return arr[1];
          }
        }
        return false;
    }
    function clearCookie(){
          var keys=document.cookie.match(/[^ =;]+(?=\=)/g);
          if (keys) {
              for (var i = keys.length; i--;)
                  document.cookie=keys[i]+'=0;expires=' + new Date( 0).toUTCString()
              }
      }
    export default {
      data() {
          var valiAccount = (rule, value, callback) => {
              if (value === '') {
                  callback(new Error('请输入旧密码'));
              } else {
                  callback();
              }
          };
          var validatePass = (rule, value, callback) => {
              var reg2 = /^([a-zA-Z0-9|])|([._`;,*-+!@#$%^&*():"'/\\]){1}([a-zA-Z0-9]|[._`;,*-+!@#$%^&*():"'/\\]){4,19}$/;
              if (value === '') {
                  callback(new Error('请输入密码'));
              } else if(value.length < 5) {
                  callback(new Error('密码长度不得小于5'));
              } else if(value.length >= 20) {
                  callback(new Error('密码长度不得大于20'));
              } else if(!reg2.test(value)) {
                  callback(new Error('密码不得包含特殊字符'));
              } else {
                  callback();
              }
          };
          var validatePass2 = (rule, value, callback) => {
              var reg2 = /^([a-zA-Z0-9|])|([._`;,*-+!@#$%^&*():"'/\\]){1}([a-zA-Z0-9]|[._`;,*-+!@#$%^&*():"'/\\]){4,19}$/;
              if (value === '') {
                  callback(new Error('请输入密码'));
              } else if(value.length < 5) {
                  callback(new Error('密码长度不得小于5'));
              } else if(value.length >= 20) {
                  callback(new Error('密码长度不得大于20'));
              } else if(!reg2.test(value)) {
                  callback(new Error('密码不得包含特殊字符'));
              } else if(value !== document.getElementById("pass1").value ){
                  callback(new Error('两次输入的密码不一致'));
              }  else {
                  callback();
              }
          };
          return {
            userName:"",
            activeName: "",
            dialogFormVisible: false,
            rules2: {
                oldpassword: [
                    { validator: valiAccount, trigger: 'blur' }
                ],
                password: [
                    { validator: validatePass, trigger: 'blur' }
                ],
                password2: [
                    { validator: validatePass2, trigger: 'blur' }
                ],
            },
            passInfo: {
                oldpassword: "",
                password: "",
                password2: ""
            },
          }
        },
      // computed: {
      //     inputSearch: function(){
      //         console.log(this.inputSearch)
      //     }
      // },
      created() {
        this.init_page();
      },
      methods: {
        init_page() {
          // 获取用户名
          this.userName = getCookie("user_account");
          this.level = getCookie("level");
        },
        // 退出登陆
        handleLogout() {
            var sendData = {
                user_account: this.userName
            };
            this.$http.post('Video_exitLogin',JSON.stringify(sendData)).then(res=>{
                if(res.status === 200) {
                    clearCookie();
                    this.$router.push("/login");
                } else {
                    this.$notify({
                        title: '失败',
                        message: res.data.msg,
                        type: 'error'
                    });
                }
            }).catch(()=>{
                this.$notify({
                    title: '错误',
                    message: '请求异常',
                    type: 'error'
                });
            })
        },
        closeDialogHandle() {
            this.$refs["passInfo"].resetFields();
        },
        // 提交表单
        subFormHandle() {
            this.$refs["passInfo"].validate((valid) => {
              if (valid) {
                var sendData = this.passInfo;
                sendData.userid = getCookie("userid");
                sendData.user_account = getCookie("user_account");
                sendData.key = getCookie("key");
                sendData.level = getCookie("level");
                this.$http.post('Video_modifyPass',JSON.stringify(sendData)).then(res=>{
                  if(res.status == 200){
                    if(res.data.header.stats === 0){
                      this.$notify({
                        title: '成功',
                        message: '修改成功，请重新登录',
                        type: 'success'
                      });
                      this.dialogFormVisible = false;
                      this.$router.push("/login");
                    } else {
                      this.$notify({
                        title: '失败',
                        message: res.data.body.list.msg,
                        type: 'error'
                      });
                    }
                  }
                }).catch(function(e){
                  console.log(e)
                })
              }
            });
        },
      }
    }

</script>
<style lang="less" scoped>
    .manage{
        overflow: hidden;
    }
    .top_nav{
        height: 60px;
        width: 100%;
        background-color: #337ab7;
        position: fixed;
        top: 0;
        z-index: 999;
        .header {
            height: 60px;
            line-height: 60px;
            color:#fff;
            .admin-title{
                text-align: left;
                font-size: 20px;
                font-weight: bold;
            }
            .userinfo{
                float: right;
                text-align: left;
                .right_handle{
                    float: right;
                }
            }
            .quit{
                color: #fff;
                margin-left: 30px;
                text-decoration: none;
            }
            .quit:hover{
                color: #ccc;
            }
        }
    }

    .side_menu{
        height: 100%;
        position: fixed;
        background-color: rgb(84, 92, 100);
        overflow: hidden;
        .el-menu{
            width: 100%;
            .el-menu-item{
                text-align: right;
                padding-right: 60px;
            }
        }
    }

    .mainer{
        margin-top: 60px;
        margin-bottom: 200px;
    }
    .dialog-footer{
        text-align: right;
    }
</style>
