import axios from "axios";
import Cookies from "js-cookie";

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";

const utils = {
  getCSRFToken: () => {
    return Cookies.get("csrftoken");
  },

  asFormData: obj => {
    Object.keys(obj).reduce((formData, key) => {
      formData.append(key, obj[key]);
      return formData;
    }, new FormData());
  }
};

export { utils, axios };
