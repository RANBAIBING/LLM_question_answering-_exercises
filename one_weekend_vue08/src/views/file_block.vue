<template>
    <div>
      <div id="top_div">

      </div>

      <div id="middle_div">
        <div class="left">
          <!-- <el-button id="add_knowledge_base_button"  type="primary" round @click="add_knowledge_base_button();">导入新文件</el-button> -->
          <el-button id="file_abackspacing_bdatabase_management"  type="primary" round @click="abackspacing_bdatabase_messagement();">返回库管理</el-button>
          <el-button id="abackspacing_bdatabase"  type="primary" round @click="abackspacing_bdatabase();">返回知识库</el-button>
          <el-button id="abackspacing_button_file_block"  type="primary" round @click="abackspacing_button();">回问答界面</el-button>
          
        </div>

        <div class="right_file_block">
            <div id="show_knowledge_base">
                <h1 id="database_name"><b>{{ file_name }}</b></h1>
                <div>
                    <div class="each_file_block" v-for="(item, index) in files_block_list">{{ item.file_chunk_content }}</div>
                    
                </div>

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
        current_file_id: 0,
        files_block_list: [],
        file_name: "文件名称",
  
      }
    },
    mounted() {
      //  alert(this.$route.query.params)
      console.log(this.$route.query.params);
      this.current_file_id = this.$route.query.params;
      // 获取数据库文件列表
      $axios.post('getallknowledgebasefilechunks/', {"file_id": this.current_file_id})
      .then(res => {
        console.log(res.code);
        if(res.code == 200) {
          this.file_name = res.file_name;
          this.files_block_list = res.knowledge_base_file_chunk_dict_list;
          console.log(res.knowledge_base_file_chunk_dict_list);
        } else{
          alert("添加失败");
        }});
    },
    methods: {
      // 添加知识库按钮
      add_knowledge_base_button() {
        alert(666)
      },
      // 返回知识库管理
      abackspacing_bdatabase_messagement() {
        this.$router.push('/database_management');
      },
      // 返回知识库
      abackspacing_bdatabase() {
        this.$router.push('/database_file');
      },
      // 返回到问答界面
      abackspacing_button() {
        this.$router.push('/');
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
    .right_file_block{
      position: absolute;
      top:0;
      right: 0;
      width: 80%;
      height: 100%;
      background-color: beige;
    }
      /* 返回知识库管理 */
      #file_abackspacing_bdatabase_management{
        position: absolute;
        left: 9%;
        top: 3%;
        width: 80%;
        height: auto;
        font-size: 30px;
      }
      #abackspacing_bdatabase{
        position: absolute;
        left: 5%;
        top: 13%;
        width: 80%;
        height: auto;
        font-size: 30px;
      }
      /* 返回到问答界面 */
      #abackspacing_button_file_block{
        position: absolute;
        left: 5%;
        top: 23%;
        width: 80%;
        height: auto;
        font-size: 30px;
      }
      /* 文件名称 */ 
      #database_name{
        text-align: center;
      }
      /* 各个文件块 */
      .each_file_block{
        border: 1px solid black;
        width: 200px;
        height: 200px;
        margin: 10px;
        padding: 5px;
        display: inline-block;
        text-align: left;
        font-size: 20px;
        overflow: auto;
        /* float: left; */

      }
      
  </style>
  