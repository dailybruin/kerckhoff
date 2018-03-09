import Vue from "vue";
import BootstrapVue from "bootstrap-vue";

// Icon imports
import "vue-awesome/icons/plus";
import "vue-awesome/icons/refresh";
import "vue-awesome/icons/search";
import "vue-awesome/icons/hdd-o";

import Icon from "vue-awesome/components/Icon";
import VueUploadComponent from "vue-upload-component";
import MainModule from "./MainModule";
import router from "./routes/ManageRoutes";

// Styles
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.component("file-upload", VueUploadComponent);
Vue.component("icon", Icon);

const mgmt = new Vue({
  router,
  el: "#app",
  components: { MainModule },
  template: "<MainModule />"
});
