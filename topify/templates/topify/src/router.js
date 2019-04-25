import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      redirect: "process"
    },
    {
      path: "/process",
      name: "process",
      component: () => import("./views/Process.vue")
    },
    {
      path: "/docker",
      name: "docker",
      component: () => import("./views/Docker.vue")
    }
  ]
});
