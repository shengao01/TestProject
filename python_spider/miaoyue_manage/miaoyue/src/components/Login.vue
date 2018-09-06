<template id="Login">
  <div class="login">
    <el-row>
      <el-col :span="6" :offset="9" class="form_warp">
        <p class="title">喵约后台运营管理平台</p>
        <el-form :model="ruleForm" status-icon :rules="rules2" ref="ruleForm" label-width="60px" class="demo-ruleForm">
          <el-form-item label="账号：" prop="user_account">
            <el-input type="text" v-model="ruleForm.user_account" class="user" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码：" prop="password">
            <el-input type="password" class="password" v-model="ruleForm.password" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')"  style="margin-left: -20px;">登录</el-button>
            <el-button @click="resetForm('ruleForm')">重置</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>
<script type="text/javascript">
  import './static/promise.js'
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
    name: "login",
    data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入用户名'));
        } else {
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('输入密码'));
        } else{
          callback();
        }
      };
      return {
        ruleForm: {
          user_account: '',
          password: ''
        },
        rules2: {
          user_account: [
            { validator: validatePass, trigger: 'blur' }
          ],
          password: [
            { validator: validatePass2, trigger: 'blur' }
          ]
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            var sendData = this.ruleForm;
            this.$http.post('Video_login',JSON.stringify(sendData)).then(res=>{
              if(res.status == 200){
                if(res.data.header.stats === 0){
                  this.$notify({
                    title: '成功',
                    message: '登陆成功',
                    type: 'success'
                  });
                  clearCookie();
                  setCookie("user_account",res.data.body.list.user_account,1);
                  setCookie("userid",res.data.body.list.userid,1);
                  setCookie("key",res.data.body.list.key,1);
                  setCookie("level",res.data.body.list.level,1);
                  window.setTimeout(()=>{
                  this.$router.push('/');
                  },1000)
                } else {
                  this.$notify({
                    title: '失败',
                    message: res.data.header.msg,
                    type: 'error'
                  });
                }
              }
            }).catch(function(e){
              console.log(e)
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>
<style media="screen" lang="less" scoped>
  .login{
    width: 100%;
    height: 100%;
    background: url(../../static/bg.jpg) no-repeat center;
    background-size: cover;
    position: fixed;
  }
  .el-row{
    margin-top: 290px;
  }
  .form_warp{
    width: 500px;
    height:360;
    padding-left: 58x;
    border: 1px solid #ccc;
    background-color: #fff;
    .title{
      width: 100%;
      font-size: 30px;
      font-weight: bold;
      margin-top: 50px;
      text-align: center;
    }
    .el-form{
      margin-top: 50px;
      width: 400px;
      .el-form-item{
        margin-bottom: 40px;

      }
    }
  }
  .el-col{
    padding-right: 60px;
  }
</style>
