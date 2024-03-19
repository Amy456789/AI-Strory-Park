module.exports = {
  publicPath: './',
  css: {
    loaderOptions: {
      postcss: {
        plugins: [require('tailwindcss'), require('autoprefixer')]
      }
    }
  },
  // devServer: {
  //   port: 8080,
  //   host: 'localhost',
  //   https: false,
  //   open: false,
  //   proxy: {
  //     '/api': {
  //       target: 'https://api.fanyi.baidu.com/api/trans/vip/translate', //设置调用的接口域名和端口
  //       changeOrigin: true, //是否跨域
  //       ws: true,
  //       pathRewrite: {
  //         '^/api': ''
  //       }
  //     }
  //   }
  // }
}
