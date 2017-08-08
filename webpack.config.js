var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,

  entry: {
    main: "./assets/js/main",
    management: "./assets/js/management"
  },

  output: {
    path: path.resolve("./assets/bundles/"),
    filename: "[name]-[hash].js"
  },

  resolve: {
    extensions: [".js", ".vue"],
    alias: {
      vue: "vue/dist/vue.js"
    }
  },

  plugins: [new BundleTracker({ filename: "./webpack-stats.json" })],

  module: {
    rules: [
      {
        test: /\.vue$/,
        use: [
          {
            loader: "vue-loader"
          }
        ]
      },
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["env"]
          }
        }
      },
      {
        test: /\.(scss|css)$/,
        use: [
          {
            loader: "style-loader" // creates style nodes from JS strings
          },
          {
            loader: "css-loader" // translates CSS into CommonJS
          },
          {
            loader: "sass-loader" // compiles Sass to CSS
          }
        ]
      }
    ]
  }
};
