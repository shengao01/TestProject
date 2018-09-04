// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
// import "babel-polyfill"
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import axios from 'axios'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI);

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

// axios.defaults.baseURL = 'http://211.149.236.46:8088/'; // 设置baseurl
axios.defaults.baseURL = 'http://172.16.30.232:85/'; // 设置baseurl
Vue.prototype.$http=axios;



router.beforeEach((to,from,next)=>{
    // 1.0 在localStorage中记录当前浏览器访问的的最后一个路由规则的名称
    if(to.name !=="login"){
    	var user_name = getCookie("user_account");
       	if(user_name) {
       		next();
       	} else {
          Vue.prototype.$notify({
            title: '失败',
            message: "请登陆后再访问",
            type: 'error'
          });
       		router.push({name:'login'});
       	}
    } else{
        // 表示不需要进行登录验证，直接访问即可
      next();
    }
});

Vue.config.productionTip = false

// Vue.use(axios);
/* eslint-disable no-new */
var vm = new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
