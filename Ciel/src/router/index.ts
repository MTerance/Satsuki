import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MainView from '../views/MainView.vue'

const router = createRouter({
  // Hash history : requis pour Electron en mode loadFile (file://),
  // où l'historique HTML5 ne résout pas les sous-routes.
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // Layout principal avec routes imbriquées.
      // MainView redirige vers 'launcher' tant que l'on n'est pas
      // connecté à une instance Satsuki (ou si aucune n'est lancée).
      path: '/',
      component: MainView,
      children: [
        { path: '', redirect: { name: 'menu' } },
        {
          path: 'menu',
          name: 'menu',
          component: () => import('../components/gameMenu/MainGameMenu.vue'),
        },
        {
          path: 'launcher',
          name: 'launcher',
          component: () => import('../views/SatsukiLauncher.vue'),
        },
        // Routes pilotées par l'état de jeu (CurrentScene du serveur Satsuki)
        {
          path: 'game/title',
          name: 'game-title',
          component: () => import('../components/gameMenu/Title.vue'),
        },
        {
          path: 'game/lobby',
          name: 'game-lobby',
          component: () => import('../components/gameMenu/Lobby.vue'),
        },
        {
          path: 'game/credits',
          name: 'game-credits',
          component: () => import('../components/gameMenu/Credits.vue'),
        },
        {
          path: 'game/main-menu',
          name: 'game-main-menu',
          component: () => import('../components/gameMenu/MainGameMenu.vue'),
        },
        {
          path: 'game/arcade',
          name: 'game-arcade',
          component: () => import('../components/gameMode/Arcade/Arcade.vue'),
        },
      ],
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/database',
      name: 'database',
      component: () => import('../components/DatabaseDemo.vue'),
    },
    {
      path: '/screen-detector',
      name: 'screen-detector',
      component: () => import('../views/ScreenDetector.vue'),
    },
    // Compatibilité avec l'ancienne URL du launcher
    {
      path: '/satsuki-launcher',
      redirect: { name: 'launcher' },
    },
  ],
})

export default router
