/* eslint-disable sort-imports */

import "./styles/tailwind.css"
import "animate.css"

import App from "./App.vue"
import { createApp } from "vue"
import router from "./router"
import store from "./store"
import icons from "@/plugins/icons.js"
import Maska from "maska"

const app = createApp(App)
app.use(store)
app.use(router)
app.use(icons)
app.use(Maska)
app.mount("#app")
