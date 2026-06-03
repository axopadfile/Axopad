import { createRouter, createWebHistory } from "vue-router";
import Discover from "@/views/Discover.vue";
import Launch from "@/views/Launch.vue";
import TokenView from "@/views/TokenView.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "Discover", component: Discover },
    { path: "/launch", name: "Launch", component: Launch },
    { path: "/token/:id", name: "Token", component: TokenView },
  ],
});
