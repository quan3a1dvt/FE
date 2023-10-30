import { boot } from "quasar/wrappers";

export default boot(({ app }) => {
    app.config.globalProperties.$ip = 'http://localhost:8080';
});
