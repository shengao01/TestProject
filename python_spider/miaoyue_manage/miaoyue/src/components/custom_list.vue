<template lang="html">
    <el-col :span="17" :offset="4">
        <el-row>
            <el-col :span="13">
                <el-breadcrumb separator-class="el-icon-arrow-right">
                    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
                    <el-breadcrumb-item>用户管理</el-breadcrumb-item>
                    <el-breadcrumb-item>{{curTableName}}</el-breadcrumb-item>
                </el-breadcrumb>
            </el-col>
            <el-col :span="8">
                <el-input
                placeholder="请输入用户手机号码"
                v-model="inputSearch">
                    <i slot="prefix" class="el-input__icon el-icon-search"></i>
                    <el-button slot="append" class="search_btn" @click="handleSearchUser">搜索</el-button>
                </el-input>
            </el-col>
            <el-col :span="3">
                <router-link :to="$route.path">
                    <el-button type="success" class="refresh">刷新</el-button>
                </router-link>
            </el-col>
        </el-row>
        <el-row class="filter_user">
            <el-col :span="2" class="xy_label">
                <span>筛选数据:</span>
            </el-col>
            <el-col :span="3">
                <el-select v-model="order_way" @change="filterFromWayHandle" placeholder="预约方式">
                    <el-option
                    v-for="item in comingWaySelect"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <!-- <el-col :span="3" :offset="1">
                <el-select v-model="test2" @change="change2" placeholder="预约服务">
                    <el-option
                    v-for="item in options4"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
            </el-col> -->
            <el-col :span="4" :offset="1">
                <div class="block">
                    <el-date-picker
                    v-model="filterDate"
                    type="daterange"
                    align="right"
                    unlink-panels
                    @change="filterDataHandle"
                    value-format="yyyy-MM-dd"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    :picker-options="pickerOptions2">
                    </el-date-picker>
                </div>
            </el-col>
        </el-row>
        <el-row class="handle_data">
            <el-col :span="2" class="xy_label">
                <span>操作:</span>
            </el-col>
            <el-col :span="2">
                <a style="color:#FFF;text-decoration:none;display:block;width:100%;height:100%;" :href="exclUrl">
                    <el-button type="primary" >一键导出excl</el-button>
                </a>
            </el-col>
        </el-row>
        <el-row class="filter_condition" v-show="dynamicTags.length>0">
            <el-col :span="2"  class="xy_label">
                <span>筛选条件:</span>
            </el-col>
            <el-col :span="22">
                <el-tag
                :key="tag.name"
                v-for="tag in dynamicTags"
                closable
                :disable-transitions="false"
                :type="tag.type"
                @close="handleCloseTag(tag)">
                {{tag.value}}
                </el-tag>
            </el-col>
        </el-row>
        <el-row class="table_wrap">
            <router-view :filterData = "JSON.stringify(filterDataObj)" @listenFromChild = "receiveChildHandle" @sendPageHandle = "initPage"></router-view>
            <div class="block">
                <el-pagination
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-sizes="[15]"
                :page-size="20"
                layout="total, sizes, prev, pager, next, jumper"
                :total="totalCount">
                </el-pagination>
            </div>
        </el-row>
	</el-col>
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
	export default {
        data () {
			return {
                exclUrl: "",
                filterData: {

                },
                // 时间筛选
                pickerOptions2: {
                    shortcuts: [{
                        text: '最近一周',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近一个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近三个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                            picker.$emit('pick', [start, end]);
                        }
                    }]
                },
                // 来源筛选
                comingWaySelect: [
                    {
                        value: '2',
                        label: '全部用户'
                    },{
                        value: '1',
                        label: '电脑用户'
                    }, {
                        value: '0',
                        label: '手机用户'
                    }
                ],
                // 当前页面
                curTableName: "",
                // s搜索的字符
                inputSearch: "",
                order_way: "",
                filterDate: "",
                dynamicTags: [],
                totalCount: 0,
                currentPage: 1,
                curExelName: "",
                filterDataObj: {
                    key: getCookie("key"),
                    user_account: getCookie("user_account")
                }
            }
        },
        methods:{
            handleSearchUser() {
                this.filterDataObj.phone = this.inputSearch;
                if(this.inputSearch) {
                    var obj = {
                        type: "success",
                        value: "手机："+this.inputSearch,
                        name: "tel"
                    };
                    this.handleAddFilterTag(obj);
                } else {
                    this.handleDeleteFilterTag("tel");
                }
            },
            // 筛选来源
            filterFromWayHandle() {
                this.filterDataObj.order_way = this.order_way;
                if(this.order_way === "0" || this.order_way === "1") {
                    var obj = {
                        type: "warning",
                        value: this.order_way === "0"? "来源：手机" : "来源：电脑",
                        name: "way"
                    };
                    this.handleAddFilterTag(obj);
                } else {
                    this.handleDeleteFilterTag("way");
                }
            },
            // 筛选日期
            filterDataHandle(val) {
                if(this.filterDate) {
                    this.filterDataObj.filter_date = this.filterDate[0] +","+ this.filterDate[1];
                    var obj = {
                        type: "",
                        value: this.filterDate[0]+" 至 "+this.filterDate[1],
                        name: "date"
                    };
                    this.handleAddFilterTag(obj);
                } else {
                    this.filterDataObj.filter_date = "";
                    this.handleDeleteFilterTag("date");
                }
            },
            // 切换页码
            handleCurrentChange(val) {
                this.currentPage = val;
                this.filterDataObj.page = this.currentPage;
            },
            // 关闭筛选标签
            handleCloseTag(val) {
                switch (val.name) {
                    case "tel":
                        this.inputSearch = "";
                        this.filterDataObj.phone = "";
                        break;
                    case "date":
                        this.filterDate = [];
                        this.filterDataObj.filter_date = "";
                        break;
                    case "way":
                        this.order_way = "2";
                        this.filterDataObj.order_way = this.order_way;
                        break;
                    default:
                        break;
                };
                this.dynamicTags.splice(this.dynamicTags.indexOf(val), 1);
            },
            // 增加筛选标签
            handleAddFilterTag(obj) {
                var fName = obj.name;
                var flag = false;
                for(var i = 0;i < this.dynamicTags.length; i++) {
                    var tagObj = this.dynamicTags[i];
                    if(tagObj.name === fName) {
                        this.dynamicTags[i]["value"] = obj.value;
                        flag = true;
                        break;
                    }
                }
                if(!flag) {
                    this.dynamicTags.push(obj);
                }
            },
            // 删除标签封装
            handleDeleteFilterTag(fName) {
                for(var i = 0;i < this.dynamicTags.length; i++) {
                    var tagObj = this.dynamicTags[i];
                    if(tagObj.name === fName) {
                        this.dynamicTags.splice(i, 1);
                        break;
                    }
                }
            },
            // 获取子组件传递过来的页码和总条数
            receiveChildHandle(data) {
                this.totalCount = Number(data.count);
                this.currentPage = Number(data.page);
                this.modifiCrumbHandle(data.componentName);
            },
            // 根据组件修改面包屑
            modifiCrumbHandle(Cname) {
                switch (Cname) {
                    case "/custom_list/confirm":
                        this.curTableName = "已确认客户";
                        this.curExelName = "secend"
                        break;
                    case "/custom_list/no_confirm":
                        this.curTableName = "未确认客户";
                        this.curExelName = "first"
                        break;
                    case "/custom_list/delete_user":
                        this.curTableName = "已删除客户";
                        this.curExelName = "third"
                        break;
                    default:
                }
                this.exclUrl = 'http://211.149.236.46:8085/Video_exportList?type='+this.curExelName+'&user_account='+getCookie("user_account")+'&key='+getCookie("key");
            },
            initPage(data) {
                this.filterDataObj.page = data.page;
            }
        }
    }
</script>

<style lang="less" scoped>
    .el-breadcrumb{
        margin-top: 30px;
    }
    .el-input{
        margin-top: 30px;
        .el-button {
            background-color: #409EFF;
            color: #fff;
        }
        .el-button:hover{
            background-color: #66b1ff;
        }
    }
    .el-menu{
        border-right: none;
    }
    .search_btn{
        margin: -15px -20px;
    }
    .refresh{
        margin-top: 30px;
    }
    .filter_user{
        margin-top: 30px;
    }
    .handle_data{
        margin-top: 30px;
    }
    .demo-table-expand {
        font-size: 0;
    }
    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }
    .demo-table-expand .el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        width: 33%;
    }
    .el-form-item .remark{
        width: 100%;
    }
    .filter_condition{
        margin-top: 30px;
        .el-tag{
            float: left;
            margin-right: 10px;
        }
        .button-new-tag {
            margin-left: 10px;
            height: 32px;
            line-height: 30px;
            padding-top: 0;
            padding-bottom: 0;
        }
        .input-new-tag {
            width: 90px;
            margin-left: 10px;
            vertical-align: bottom;
        }
    }
    .el-pagination{
        margin-top: 30px;
    }
    .xy_label{
        line-height: 40px;
        text-align: left;
    }
    .table_wrap{
        padding-top: 30px;
    }
</style>
