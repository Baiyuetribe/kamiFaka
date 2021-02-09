import { DirectiveBinding } from 'vue';
import { LazyOptions, Target } from '../types';
import ImageManager from './imageManager';
export default class Lazy {
    error: string;
    loading: string;
    cache: Set<string>;
    managerQueue: ImageManager[];
    observer?: IntersectionObserver;
    targetQueue?: Target[];
    throttleLazyHandler: Function;
    constructor(options: LazyOptions);
    add(el: HTMLElement, binding: DirectiveBinding): void;
    update(el: HTMLElement, binding: DirectiveBinding): void;
    remove(el: HTMLElement): void;
    private init;
    private initIntersectionObserver;
    private addListenerTarget;
    private removeListenerTarget;
    private addListener;
    private removeListener;
    private lazyHandler;
    private removeManager;
}
