import { ImageManagerOptions, State } from '../types';
export default class ImageManager {
    el: HTMLElement;
    parent: HTMLElement | Window;
    src: string;
    error: string;
    loading: string;
    cache: Set<string>;
    state: State;
    constructor(options: ImageManagerOptions);
    load(next?: Function): void;
    isInView(): boolean;
    update(src: string): void;
    private renderSrc;
    private render;
}
