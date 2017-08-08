import Vue from "vue";
import Router from "vue-router";
import Display from "../components/Display";

Vue.use(Router);

const routes = [
  {
    path: "/",
    component: Display
  }
];

export default new Router({
  mode: "history",
  routes
});
