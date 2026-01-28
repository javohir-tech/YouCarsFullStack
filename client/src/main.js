import './assets/main.css'
import './assets/base.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
//Antd
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
//PINIA
import { createPinia } from 'pinia'

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(Antd)
app.mount('#app')
