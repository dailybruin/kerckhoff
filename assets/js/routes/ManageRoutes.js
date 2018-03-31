import Vue from "vue";
import Router from "vue-router";
import UserProfile from "../components/UserProfile";
import Manage from "../components/Manage";
import ManageDisplay from "../components/management/ManageDisplay";
import NewSite from "../components/management/NewSite";
import NewSiteForm from "../components/management/NewSiteForm";
import Packages from "../components/management/Packages";
import PackageView from "../components/management/PackageView";

Vue.use(Router);

const routes = [
  {
    path: "/accounts/profile",
    component: UserProfile
  },
  {
    path: "/manage",
    component: Manage,
    children: [
      {
        path: "",
        component: ManageDisplay
      },
      {
        path: "new",
        component: NewSiteForm
      },
      {
        path: "packages",
        component: Packages
      },
      {
        path: "packages/:slug",
        component: PackageView
      }
    ]
  }
];

export default new Router({
  mode: "history",
  routes
});
