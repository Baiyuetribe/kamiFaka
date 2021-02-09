import { App } from 'vue';
import { LazyOptions } from './types';
declare const lazyPlugin: {
    install(app: App<any>, options: LazyOptions): void;
};
export default lazyPlugin;
