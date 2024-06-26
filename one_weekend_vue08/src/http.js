// src/axios.js  
import axios from 'axios';  
  
const $axios = axios.create({  
  baseURL: 'http://127.0.0.1:8000/', // 设置基础 URL  
  timeout: 20000, // 设置请求超时时间  
  headers: { 'Content-Type': 'application/json' }, // 设置默认 headers  
});  
  
// 添加请求拦截器  
$axios.interceptors.request.use(  
  config => {  
    // 在发送请求之前做些什么  
    // 例如，你可以在这里添加认证 token  
    return config;  
  },  
  error => {  
    // 对请求错误做些什么  
    return Promise.reject(error);  
  }  
);  
  
// 添加响应拦截器  
$axios.interceptors.response.use(  
  response => {  
    // 对响应数据做点什么  
    return response.data; // 假设服务器返回的数据在 data 属性中  
  },  
  error => {  
    // 对响应错误做点什么  
    return Promise.reject(error);  
  }  
);  
  
export default $axios;