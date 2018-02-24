import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import Icon from "vue-awesome/components/Icon";
import "vue-awesome/icons";
import MainModule from "./MainModule";
import router from "./routes/MainRoutes";
import utils from "./util";

// Styles
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.component("icon", Icon);

/* eslint-disable no-new */
const app = new Vue({
  router,
  el: "#app",
  template: "<MainModule />",
  components: { MainModule }
});
