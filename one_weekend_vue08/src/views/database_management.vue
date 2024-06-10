<template>
    <div>
      <div id="top_div">

      </div>

      <div id="middle_div">
        <div class="left">
          <el-button id="add_knowledge_base_button"  type="primary" round @click="add_database_show_button();">添加知识库</el-button>
          <el-button id="abackspacing_button"  type="primary" round @click="abackspacing_button();">回问答界面</el-button>
          <div id="add_database_div" :style="add_database_display">
            库的名称<br><input class="new_add_database_content" v-model="new_database_name" type="text" placeholder="输入4字以内名称"><br>
            分块的小<br><input class="new_add_database_content" v-model="new_database_size" type="number" placeholder="输入分块大小"><br>
            重复数量<br><input class="new_add_database_content" v-model="new_database_renum" type="number" placeholder="输入重复数量"><br>
            <el-button type="primary" @click="add_new_database();">添加</el-button>

          </div>
          
        </div>

        <div class="right">
          <div id="show_knowledge_base">
            <h1 id="database_name"><b>知识库列表</b></h1>
            <table>
              <thead>
                <tr>
                  <th>序号</th>
                  <th>知识库名称</th>
                  <th>创建时间</th>
                  <th>分块大小</th>
                  <th>重复数量</th>
                  <th>操作</th>
                </tr>
              </thead>
              
              <tbody>
                <tr  v-for="(item, index) in database_list">
                  <td>{{ index+1 }}</td>
                  <td>{{ item.knowledge_base_name }}</td>
                  <td>{{ item.create_time }}</td>
                  <td>{{ item.maximum_block_length }}</td>
                  <td>{{ item.repeated_character_length }}</td>
                  <td>
                    <el-button type="primary" @click="look_database(item.id);">查看</el-button>
                    <!-- <el-button type="primary" :icon="Edit" circle /> -->
                    <el-button type="danger" :icon="Delete" circle @click="deleting_knowledge_base(item.id);" />
                  </td>
                </tr>

              </tbody>
            </table>
          </div>
        </div>
       
      </div>


        
    </div>
  
  </template>
  
  <script>
  import $axios from "../http";
  import { Check,Delete,Edit,Message,Search,Star, } from '@element-plus/icons-vue';
  export default {
    data() {
      return {
        Check,Delete,Edit,Message,Search,Star,
        add_database_display: "display: none;",
        new_database_name: "",
        new_database_size: 100,
        new_database_renum: 0,
        current_database_id: 0,
        database_list: [],
  
      }
    },
    mounted() {
      // 刷新数据库列表
      $axios.get('getallknowledgebases/')
      .then(res => {
        console.log(res.code);
        if(res.code == 200) {
          this.database_list = res.knowledge_base_list;
          console.log(res.code);
        } else{
          alert("获取失败");
        }});
    },
    methods: {
      // 添加知识库按钮
      add_database_show_button() {
        this.add_database_display = "display: block;";
      },
      // 返回到问答界面
      abackspacing_button() {
        this.$router.push('/');
      },
      // 查看知识库文件
      look_database(database_id) {
        // this.$router.push('/database_file?kk=6');
        this.$router.push({ path: '/database_file', query: {params:database_id}, });
      },
      // 刷新知识库列表
      refresh_database_list() {
        // 刷新数据库列表
        $axios.get('getallknowledgebases/')
        .then(res => {
          console.log(res.code);
        if(res.code == 200) {
          this.database_list = res.knowledge_base_list;
          console.log(res.code);
        } else{
          alert("获取失败");
        }});
      },
      // 添加新知识库
      add_new_database() {
        // alert("添加功能待实现")
        var cont = {
          database_name: this.new_database_name,
          database_size: this.new_database_size,
          database_renum: this.new_database_renum,
        }
        $axios.post('newknowledgebases/', cont)
        .then(res => {
          console.log(res.data);
          if(res.code == 200) {
            // alert("添加成功");
            console.log(res.msg);
            this.refresh_database_list();
            this.add_database_display = "display: none;";
          } else{
            alert("添加失败");
          }});
      },
      // 删除知识库
      deleting_knowledge_base(database_id) {
        // alert("删除功能待实现")
        var cont = {
          database_id: database_id,
        }
        $axios.post('deleteknowledgebases/', cont)
        .then(res => {
          console.log(res.code);
          if(res.code == 200) {
            // alert("删除成功");
            console.log(res.msg);
            this.refresh_database_list();
          }
          else{
              // alert("删除失败");
              console.log(res.msg);
          }});
      },
      // 临时测试函数
      temps() {
        alert(666)
      },
    }
  }
  </script>
  
  <style>
    *{
        margin: 0px;
        padding: 0px;
      }
      html,body{
        width: 100%;
        height: 100%;
        background-color: beige;

      }
      /* 顶部div边框 */
    #top_div{
      position: absolute;
      top: 0%;
      left: 0%;
      width: 100%;
      height: 8%;
      background-color: rgb(244, 244, 185);
      border: 2px solid black;
    }
    /* 中间div边框 */
    #middle_div{
      position: absolute;
      left: 0%;
      top: 8%;;
      width: 100%;
      height: 92%;
      
    }

    /* 左边大边框 */
    .left{
      position: absolute;
      left: 0;
      top: 0;
      width: 20%;
      height: 100%;
      background-color: gray;
    }
    /* 右边大边框 */
    .right{
      position: absolute;
      top:0;
      right: 0;
      width: 80%;
      height: 100%;
      background-color: beige;
      text-align: center;
    }
      /* 展示知识库 */
      #show_knowledge_base{
        border: 2px solid black;
        position: absolute;
        top: 2%;
        left: 1%;
        width: 98%;
        height: 96%;
        color: black;
        /* display: none; */
        overflow: auto;
        font-size: 20px;
        padding: 10px;
        
      }
      /* 添加知识库按钮 */
      #add_knowledge_base_button{
        position: absolute;
        left: 9%;
        top: 3%;
        width: 80%;
        height: auto;
        font-size: 30px;
      }
      /* 返回到问答界面 */
      #abackspacing_button{
        position: absolute;
        left: 5%;
        top: 13%;
        width: 80%;
        height: auto;
        font-size: 30px;
      }
      /* 知识库名称 */
      #database_name{
        
        
      }
      /* 表格 */
      table{
        position: absolute;
        left: 2%;
        top: 14%;
        width: 96%;
        border: 1px solid black;
        /* border-collapse: collapse; */
      }
      /* 表头与表行 */
      th, td{
        border: 1px solid black;
        /* border-collapse: collapse; */
        text-align: center;
      }
      /* 添加知识库的输入内容显示div */
      #add_database_div{
        border: 1px solid black;
        position: absolute;
        left: 3%;
        top: 30%;
        width: 94%;
        height: 55%;
        padding: 10px;
        font-size: 30px;
        color: black;
        text-align: center;
      }
      /* 添加知识库的输入内容显示样式 */
      .new_add_database_content{
        width: 90%;
        height: 35px;
        font-size: 25PX;
      }

      
  </style>
  