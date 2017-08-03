import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import App from "./App";

// Styles
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);

/* eslint-disable no-new */
const app = new Vue({
  el: "#app",
  template: "<App/>",
  components: { App }
});
