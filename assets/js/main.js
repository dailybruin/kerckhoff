import Vue from "vue";
import BootstrapVue from "bootstrap-vue";

// Icon imports
import "vue-awesome/icons/plus";
import "vue-awesome/icons/refresh";
import "vue-awesome/icons/search";

import Icon from "vue-awesome/components/Icon";
import MainModule from "./MainModule";
import router from "./routes/MainRoutes";
import utils from "./util";

// Styles
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

//Vue Layout Import
import { VueMasonryPlugin } from "vue-masonry";

Vue.use(BootstrapVue);
Vue.component("icon", Icon);
Vue.use(VueMasonryPlugin);

/* eslint-disable no-new */
const app = new Vue({
  router,
  el: "#app",
  template: "<MainModule />",
  components: { MainModule }
});
