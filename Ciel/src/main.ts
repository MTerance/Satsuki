import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Ensure the DaisyUI theme 'ciel' is applied globally.
// Index.html already contains `data-theme="ciel"`, but we enforce it at runtime
// so all pages get the template even if the attribute was accidentally removed.
if (typeof document !== 'undefined') {
	const html = document.documentElement
	if (html.getAttribute('data-theme') !== 'ciel') {
		html.setAttribute('data-theme', 'ciel')
	}
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
