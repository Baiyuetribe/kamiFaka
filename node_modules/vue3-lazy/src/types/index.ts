export enum State {
  loading,
  loaded,
  error
}

export interface LazyOptions {
  error?: string
  loading?: string
}

export interface ImageManagerOptions {
  el: HTMLElement
  parent: HTMLElement | Window
  src: string
  error: string
  loading: string
  cache: Set<string>
}

export interface Target {
  el: HTMLElement | Window
  ref: number
}

