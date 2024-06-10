<template>
  <div>
    <div id="top_div">

    </div>


    <div id="middle_div">
    <div class="left">
      <el-button id="new_speak"  type="primary" round @click="create_new_session();">新建会话</el-button>
      <!-- <button  @click="temps();">测试</button> -->
      <input id="search_history"type="text" v-model="search_history_content" placeholder="搜索历史记录"><el-button id="search_history_button" @click="search_history_conversation();" :icon="Search" circle />
      <div id="history_show">
        <ul id="history_show_list">
          <li v-for="(item,index) in history_conversation" :key="index">
            <button class="history_show_list_button" @click="history_transfer(item.id);">{{ item.show_content }}</button>&nbsp;
            <el-button class="delete_history_session" @click="delete_history_session(item.id);" type="danger" :icon="Delete" circle />
          </li>
        </ul>
      </div>
    </div>
    
    <div class="right">
      <div class="left2">
        <!-- <p id="model_class">通义千问</p> -->
        <!-- <el-button id="ali_model_class" type="primary" plain>通义千问</el-button> -->
        <!-- <el-button id="baidu_model_class" type="primary" plain>文心一言</el-button> -->
        <select id="model_class_select" name="model_class_select" @click="model_class_select();">
          <option value="baidu_wenxin">文心一言</option>
          <option value="ali_tongyi">通义千问</option>
          <option value="RAG_knowledge_base">知识库</option>
        </select>
        <!-- <el-button @click="temps" type="primary">数据库管理</el-button> -->
        <!-- <button @click="database_management();">数据库管理</button> -->
        <el-button id="database_management_button" :style="display"  @click="database_management();" type="primary">数据库管理</el-button>

        <div id="selectable_databases" :style="display">
          <ul id="selectable_databases_list">
            <li><el-button class="selectable_databases_list_button" type="success" v-for="(item, index) in knowledge_base_list" @click="switching_knowledge_base(item.id, item.knowledge_base_name);">{{ item.knowledge_base_name }}</el-button></li>
            
          </ul>
        </div>
        
      </div>
      <div class="right">
        <div id="answer_content">

        </div>
        <div id="problem_search">
          <input id="problem_search_text" type="text" placeholder="请输入要询问的问题">&nbsp;&nbsp;
          <el-button id="button" @click=select_model type="primary">询问</el-button>
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
      baidu_age_answer: [],
      baidu_num: 0,
      // cont: {"question":"你好", "age_answer":""}
      ali_age_answer: [],
      ali_num: 0,
      select_model: this.baidu_question,
      is_first_click: true,
      history_conversation: [],  // 历史会话窗
      current_session_id: 0,
      search_history_content: "",
      display: "display: none;",
      knowledge_base_list: [],
      current_knowledge_base_id: 0,
    }
  },
  mounted() {
    // 获取历史会话窗
    $axios.get('windows/')
    .then(response => {  
      // 处理响应数据  
      if(response.history_list.length!=0){
        this.history_conversation=response.history_list
        this.current_session_id = response.history_list[0].id
        // alert(response.history_list[0].id)
        this.history_transfer(this.current_session_id);
      }else{
        // 创建第一个新窗口
        this.create_new_session();
      }
    })  
    .catch(error => {  
      // 处理请求错误  
      console.error(error);  
    }); 
    // alert(this.current_session_id)
     
  },
  methods: {
    // 百度多轮智能问答
    baidu_question(){
      var cont={
        question:null,
        // age_answer:"",
        session_id: this.current_session_id
      };
      var question=document.getElementById("problem_search_text");
      cont.question=question.value;
      // for(var i=0;i<this.baidu_age_answer.length;i++){
      //     cont.age_answer += this.baidu_age_answer[i].question+"&"+this.baidu_age_answer[i].content +"&";
      // }

      var div_answer=document.getElementById("answer_content");
      div_answer.innerText += "问题：" + question.value+"\n\n";
      div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部

      $axios.post('baidus/', cont)
      .then(response => {  
        // 处理响应数据  
        console.log(response.content);
        var div_answer=document.getElementById("answer_content");
        div_answer.innerText += "回答：" + response.content+"\n\n";
        div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
        // this.baidu_age_answer[this.baidu_num] = {'question':question.value,'content':response.content};
        // this.baidu_num += 1;
        this.update_history_list();
      })  
      .catch(error => {  
        // 处理请求错误  
        console.error(error);  
      });  
        
    },
    // 阿里多轮问答
    ali_question(){
      var cont={
          question:null,
          // age_answer:"",
          session_id: this.current_session_id
      };
      var question=document.getElementById("problem_search_text");
      cont.question=question.value;
      // for(var i=0;i<this.ali_age_answer.length;i++){
      //     cont.age_answer+= this.ali_age_answer[i].question+"&"+this.ali_age_answer[i].content +"&";
      // }
  
      var div_answer=document.getElementById("answer_content");
      div_answer.innerText += "问题：" + question.value+"\n\n";
      div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
      
      $axios.post('alis/', cont)
      .then(response => {  
        // 处理响应数据  
        console.log(response.content);
        var div_answer=document.getElementById("answer_content");
        div_answer.innerText += "回答：" + response.content+"\n\n";
        div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
        // this.ali_age_answer[this.ali_num] = {'question':question.value,'content':response.content};
        // this.ali_num += 1;
        this.update_history_list();
      })  
      .catch(error => {  
        // 处理请求错误  
        console.error(error);  
      });  

    },
    // 基于知识库的阿里大模型单论问答
    knowledge_base_ali_question(){
      var cont={
          question:null,
          // age_answer:"",
          session_id: this.current_session_id,
          knowledge_base_id: this.current_knowledge_base_id
      };
      var question=document.getElementById("problem_search_text");
      cont.question=question.value;
      // for(var i=0;i<this.ali_age_answer.length;i++){
      //     cont.age_answer+= this.ali_age_answer[i].question+"&"+this.ali_age_answer[i].content +"&";
      // }
  
      var div_answer=document.getElementById("answer_content");
      div_answer.innerText += "问题：" + question.value+"\n\n";
      div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
      
      $axios.post('knowledgebases/', cont)
      .then(response => {  
        // 处理响应数据  
        console.log(response.content);
        var div_answer=document.getElementById("answer_content");
        div_answer.innerText += "回答：" + response.content+"\n\n";
        div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
        // this.ali_age_answer[this.ali_num] = {'question':question.value,'content':response.content};
        // this.ali_num += 1;
        this.update_history_list();
      })  
      .catch(error => {  
        // 处理请求错误  
        console.error(error);  
      });  
    },


    // 大模型类型切换
    model_class_select(){
      if(this.is_first_click){
        this.is_first_click=false
      }else{
        var select_model_class=document.getElementById("model_class_select");
        if(select_model_class.value == "baidu_wenxin"){
          this.select_model = this.baidu_question;
          this.display = "display: none;"

          var div_answer=document.getElementById("answer_content");
          div_answer.innerText += "提示：已为您切换为百度文心一言"+"\n\n";
          div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
          $axios.post('hints/', {"hint_content": "已为您切换为百度文心一言", "session_id": this.current_session_id})
            .then(response => {  
              // 处理响应数据  
              console.log(response);  
            })  
            .catch(error => {  
              // 处理请求错误  
              console.error(error);  
          });

          console.log(select_model_class.value); 
        }else if(select_model_class.value == "ali_tongyi"){
          this.select_model = this.ali_question;
          this.display = "display: none;"

          var div_answer=document.getElementById("answer_content");
          div_answer.innerText += "提示：已为您切换为阿里通义千问"+"\n\n";
          div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
          $axios.post('hints/', {"hint_content": "已为您切换为阿里通义千问", "session_id": this.current_session_id})
            .then(response => {  
              // 处理响应数据  
              console.log(response);  
            })  
            .catch(error => {  
              // 处理请求错误  
              console.error(error);  
          });

          console.log(select_model_class.value); 
        }else if(select_model_class.value == "RAG_knowledge_base"){
          this.select_model = this.knowledge_base_ali_question;
          this.display = "display: block;"
          
          var div_answer=document.getElementById("answer_content");
          div_answer.innerText += "提示：已为您切换为基于知识库的阿里大模型问答"+"\n\n";
          div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
          $axios.post('hints/', {"hint_content": "已为您切换为基于知识库的阿里大模型问答", "session_id": this.current_session_id})
            .then(response => {  
              // 处理响应数据  
              console.log(response);  
            })  
            .catch(error => {  
              // 处理请求错误  
              console.error(error);  
          });

          // 获取知识库列表
          $axios.get('getallknowledgebases/')
          .then(res => {
            console.log(res.code);
          if(res.code == 200) {
            this.knowledge_base_list = res.knowledge_base_list;
            this.current_knowledge_base_id=knowledge_base_list[0].id;
            console.log(res.code);
          } else{
            alert("获取失败");
          }});

      }
        this.is_first_click=true
      }
      
    },
    // 创建新会话
    create_new_session(){
      $axios.post('windows/')
        .then(response => {  
          // 处理响应数据  
          console.log(response);  
          var div_answer=document.getElementById("answer_content");
          div_answer.innerText = "";
          this.current_session_id = response.new_session_id;
          // alert(this.current_session_id)
          this.update_history_list();
      
        })  
        .catch(error => {  
          // 处理请求错误  
          console.error(error);  
      });
    },
    // 点击历史会话进行跳转
    history_transfer(session_id) {
      this.current_session_id = session_id;
      // alert(this.current_session_id);
      $axios.post('windowsid/', {"session_id": session_id})
        .then(response => {  
          // 处理响应数据  
          console.log(response);  
          var div_answer=document.getElementById("answer_content");
          div_answer.innerText = "";
          for(var i=0;i<response.records_list.length;i++){
            div_answer.innerText += response.records_list[i]+"\n\n";
            div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
          }

        })  
        .catch(error => {  
          // 处理请求错误  
          console.error(error);  
      });  
    },
    // 删除历史会话
    delete_history_session(session_id){
      // alert(session_id);
      $axios.post('deletes/', {"session_id": session_id})
        .then(response => {  
          // 处理响应数据  
          console.log(response);  
          this.update_history_list();
          this.history_transfer(this.current_session_id);

        })  
        .catch(error => {  
          // 处理请求错误  
          console.error(error);  
      });  
    },
    // 刷新历史会话展示列表
    update_history_list() {
    // 获取历史会话窗
    $axios.get('windows/')
      .then(response => {  
        // 处理响应数据  
        if(response.history_list.length!=0){
          this.history_conversation=response.history_list
          var not_have_current_session=true;
          for(var i=0;response.history_list.length;i++){
            if(response.history_list[i].session_id==this.current_session_id){
              not_have_current_session=false;
            }
          }
          if(not_have_current_session){
            this.current_session_id = response.history_list[0].session_id;
          }
        }else{
          this.history_conversation=[];
        }
      })  
      .catch(error => {  
        // 处理请求错误  
        console.error(error);  
      }); 
    },
    // 搜索历史会话
    search_history_conversation(){
      // alert(this.search_history_content)
      $axios.post('searchs/', {"search_content": this.search_history_content})
      .then(response => {  
        // 处理响应数据  
        console.log(response);  
        if(response.search_history_list.length!=0){
          this.history_conversation=response.search_history_list
        }

      })  
      .catch(error => {  
        // 处理请求错误  
        console.error(error);  
      });  
    },
    // 知识库管理
    database_management() {
      this.$router.push('/database_management');
    },
    // 切换知识库
    switching_knowledge_base(knowledge_base_id, knowledge_base_name) {
      this.current_knowledge_base_id = knowledge_base_id;

      var div_answer=document.getElementById("answer_content");
          div_answer.innerText += "提示：已为您切换为基于"+knowledge_base_name+"知识库的阿里大模型问答"+"\n\n";
          div_answer.scrollTop = div_answer.scrollHeight; // 滚动到底部
          $axios.post('hints/', {"hint_content": "已为您切换为基于"+knowledge_base_name+"知识库的阿里大模型问答", "session_id": this.current_session_id})
            .then(response => {  
              // 处理响应数据  
              console.log(response);  
            })  
            .catch(error => {  
              // 处理请求错误  
              console.error(error);  
          });

    },
    // 临时测试函数
    temps() {
      alert(666)
      $axios.get('baidus/')
      .then(data => {  
        // 处理响应数据  
        console.log(data);  

        var select_model_class=document.getElementById("model_class_select");
        console.log(select_model_class.value); 

      })  
      .catch(error => {  
        // 处理请求错误  
        console.error(error);  
      });  
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
    /* 右边大边框中的左边大边框 */
    .left2{
      width: 15%;
      height: 100%;
      background-color: beige;
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
    /* 问题搜索div */
    #problem_search{
      /* text-align: center; */
      position: absolute;
      width: 100%;
      top:90%;
      
    }
    /* 问题内容输入框 */
    #problem_search_text{
      position: absolute;
      left: 5%;
      width: 70%;
      font-size: 25px;
    }
    /* 提交问题按钮 */
    #button{
      position: absolute;
      left: 76%;
      font-size: 25px;
    }
    /* 大模型类型选择框 */
    #model_class_select{
      position: absolute;
      left: 5%;
      top: 3%;
      color: black;
      font-size: 30px;
      background-color:aqua
    }
    /* 问答显示框 */
    #answer_content{
      border: 2px solid black;
      position: absolute;
      top: 5%;
      left: 5%;
      width: 80%;
      height: 80%;
      color: black;
      /* display: none; */
      overflow: auto;
      font-size: 20px;
      padding: 10px;
      
    }
    /* 问答会话历史搜索 */
    #search_history{
      position: absolute;
      top: 12%;
      left: 15px;
      font-size: 30px;
      width: 90%;
      
    }
    /* 新建会话 */
    #new_speak{
      position: absolute;
      left: 18%;
      top: 3%;
      width: 60%;
      height: 6%;
      font-size: 30px;
    }
    /* 历史会话展示框 */
    #history_show{
      border: 1px solid black;
      position: absolute;
      left: 2%;
      top: 20%;
      width: 96%;
      height: 78%;
      font-size: 30px;
      color: black;
      padding: 10px;
      overflow: auto;
    }
    /* 历史会话展示列表 */
    #history_show_list{
      /* border: 1px solid black; */
      position: absolute;
      left: 3%;
      /* top: 20%; */
      /* width: 96%;
      height: 78%; */
      font-size: 30px;
      color: black;
    }
    /* 历史会话窗跳转按钮 */
    .history_show_list_button{
      width: 210px;
      font-size: 30px;
      
    }
    /* 删除历史会话 */
    .delete_history_session{
      
    }
    /* 可选知识库展示(div) */
    #selectable_databases{
      border: 1px solid black;
      position: absolute;
      left: 5%;
      top: 17%;
      width: 12%;
      height: 81%; 
      font-size: 30px;
      color: black;
      overflow: auto;
    }
    /* 可选知识库列表展示 */
    #selectable_databases_list{
      list-style-type: none; 
    }
    /* 可选知识库列表按钮 */
    .selectable_databases_list_button{
      width: 120px;
      height: 35px;
      font-size: 25px;
    }
    
    #search_history_button{
      position: absolute;
      top: 12.5%;
      left: 80%;
    }
    #database_management_button{
      position: absolute;
      top: 10%;
      left: 5%;
      font-size: 20px;
      width: 12%;
      height: auto;
      
    }
</style>
