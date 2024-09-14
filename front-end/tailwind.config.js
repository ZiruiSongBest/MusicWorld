/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}', // 添加项目中所有可能包含 Tailwind CSS 类的文件
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1DA1F2', // 添加自定义颜色
        secondary: '#14171A',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // 添加自定义字体
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'), // 如果需要 Tailwind 表单插件
    require('@tailwindcss/typography'), // 如果需要排版插件
  ],
}
