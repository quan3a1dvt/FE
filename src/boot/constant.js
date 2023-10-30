import { boot } from "quasar/wrappers";

export default boot(({ app }) => {
    app.config.globalProperties.$ip = 'https://4c93-2a09-bac5-d45d-2c8-00-47-2f2.ngrok-free.app';
});
