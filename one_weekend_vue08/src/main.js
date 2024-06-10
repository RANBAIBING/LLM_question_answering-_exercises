import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// element-plus配置
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

// 访问后端
// import axios from 'axios'

const app = createApp(App)

// element-plus配置
app.use(ElementPlus)

// 加入后端
// app.provide('$axios',axios)

app.use(createPinia())
app.use(router)

app.mount('#app')
