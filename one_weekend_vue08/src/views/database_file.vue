<template>
    <div>
      <div id="top_div">

      </div>

      <div id="middle_div">
        <div class="left">
          <el-button id="add_knowledge_base_button"  type="primary" round @click="add_file_show_button();">导入新文件</el-button>
          <el-button id="abackspacing_bdatabase_file"  type="primary" round @click="abackspacing_bdatabase();">返回库管理</el-button>
          <el-button id="abackspacing_button_file"  type="primary" round @click="abackspacing_button();">回问答界面</el-button>
          <div id="add_file_div" :style="add_file_display">
            添加文件<br><input class="new_add_file_content" type="file" accept=".txt, .pdf, .docx" @change="uploadFile" /><br>
            <p id="comment_content">注：支持txt、pdf、docx文件格式。</p>
            <el-button type="primary" @click="add_new_file();">添加</el-button>

          </div>
          
        </div>

        <div class="right">
            <div id="show_knowledge_base">
                <h1 id="database_name"><b>{{ database_name }}</b></h1>
            <table>
              <thead>
                <tr>
                  <th>序号</th>
                  <th>文件名称</th>
                  <th>文件类型</th>
                  <th>创建时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              
              <tbody>
                <tr v-for="(item, index) in files_list">
                  <td>{{ index+1 }}</td>
                  <td>{{ item.file_name }}</td>
                  <td>{{ item.file_type }}</td>
                  <td>{{ item.create_time }}</td>
                  <td>
                    <el-button type="primary" @click="look_file_block(item.id);">查看</el-button>
                    <!-- <el-button type="primary" :icon="Edit" circle /> -->
                    <el-button type="danger" :icon="Delete" circle />
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
        add_file_display: "display: none;",
        cont: {
          myfile: "",
          database_id: 0,
        },
        current_database_id: 0,
        files_list: [],
        database_name: "知识库名称",
      
  
      }
    },
    mounted() {
      // alert(this.$route.query.params)
      console.log(this.$route.query.params);
      this.current_database_id = this.$route.query.params;
      // 获取数据库文件列表
      $axios.post('getallknowledgebasefiles/', {"database_id": this.current_database_id})
      .then(res => {
        console.log(res.code);
        if(res.code == 200) {
          this.database_name = res.knowledge_base_name;
          this.files_list = res.knowledge_base_file_dict_list;
          console.log(res.knowledge_base_file_dict_list);
        } else{
          alert("添加失败");
        }});
    },
    methods: {
      // 添加文件显示按钮
      add_file_show_button() {
        this.add_file_display = "display: block;";
      },
      // 获取文件
      uploadFile(event) {
        this.cont.myfile = event.target.files[0];
        this.cont.database_id = this.current_database_id;
      },
      // 刷新文件列表
      refresh_file_list() {
        // 刷新文件列表
        $axios.post('getallknowledgebasefiles/', {"database_id": this.current_database_id})
        .then(res => {
          console.log(res.code);
        if(res.code == 200) {
          this.files_list = res.knowledge_base_file_dict_list;
          console.log(res.knowledge_base_file_dict_list);
        } else{
          alert("添加失败");
        }});
     },
      // 添加新文件按钮
      add_new_file(event) {
        // alert("添加功能待实现")
        // 添加文件提交  
        this.add_file_display = "display: none;";
        $axios.post('files/', this.cont, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        // $axios.post('knowledgebases/', cont)
        .then(response => {  
          // 处理响应数据  
          alert("文件添加成功");
          console.log(response.msg);
          this.refresh_file_list();
          })  
        .catch(error => {  
          // 处理请求错误  
          console.error(error);  
        });  
      },
      // 返回知识库
      abackspacing_bdatabase() {
        this.$router.push('/database_management');
      },
      // 返回到问答界面
      abackspacing_button() {
        this.$router.push('/');
      },
      // 查看文件分块
      look_file_block(file_id) {
        // this.$router.push('/file_block');
        this.$router.push({ path: '/file_block', query: {params:file_id}, });
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
      /* 返回知识库 */
      #abackspacing_bdatabase_file{
        position: absolute;
        left: 5%;
        top: 13%;
        width: 80%;
        height: auto;
        font-size: 30px;
      }
      /* 返回到问答界面 */
      #abackspacing_button_file{
        position: absolute;
        left: 5%;
        top: 23%;
        width: 80%;
        height: auto;
        font-size: 30px;
      }
      /* 添加文件的输入内容显示div */
      #add_file_div{
        border: 1px solid black;
        position: absolute;
        left: 3%;
        top: 35%;
        width: 94%;
        height: 30%;
        padding: 10px;
        font-size: 30px;
        color: black;
        text-align: center;
      }
      /* 添加文件的输入内容显示样式 */
      .new_add_file_content{
        position: absolute;
        top: 70px;
        left: 35px;
        font-size: 20px;
      }
      #comment_content{
        font-size: 12px;
      }
      
  </style>
  