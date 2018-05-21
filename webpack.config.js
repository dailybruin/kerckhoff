var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,

  mode: process.env.DEBUG == "True" ? "development" : "production",

  entry: {
    main: "./kerckhoff/assets/js/main",
    management: "./kerckhoff/assets/js/management"
  },

  output: {
    path: path.resolve("./kerckhoff/assets/bundles/"),
    filename: "[name]-[hash].js"
  },

  resolve: {
    extensions: [".js", ".vue"],
    alias: {
      vue: "vue/dist/vue.js"
    }
  },

  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: "common",
          chunks: "all"
        }
      }
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
