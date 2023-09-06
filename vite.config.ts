import { defineConfig } from "vite";
import reactRefresh from "@vitejs/plugin-react-refresh";

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    outDir: "build",
  },
  plugins: [reactRefresh()],
  define: {
    "process.env.RUN_ENV": JSON.stringify(""),
  },
  resolve: {
    alias: [{ find: /^~/, replacement: "" }],
  },
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
        modifyVars: { "@icon-font-path": "./fonts" }, // copied the files from node_modules/rsuite/es/styles/fonts to get around build issues
      },
    },
  },
  server: {
    host: "127.0.0.1",
  },
});
