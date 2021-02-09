import { ImageManagerOptions, State } from '../types'
import loadImage from '../helpers/loadImage'
import { warn } from '../helpers/debug'

export default class ImageManager {
  el: HTMLElement
  parent: HTMLElement | Window
  src: string
  error: string
  loading: string
  cache: Set<string>
  state: State

  constructor (options: ImageManagerOptions) {
    this.el = options.el
    this.parent = options.parent
    this.src = options.src
    this.error = options.error
    this.loading = options.loading
    this.cache = options.cache
    this.state = State.loading

    this.render(this.loading)
  }

  load (next?: Function): void {
    if (this.state > State.loading) {
      return
    }
    if (this.cache.has(this.src)) {
      this.state = State.loaded
      this.render(this.src)
      return
    }
    this.renderSrc(next)
  }

  isInView (): boolean {
    const rect = this.el.getBoundingClientRect()
    return rect.top < window.innerHeight && rect.left < window.innerWidth
  }

  update (src: string): void {
    const currentSrc = this.src
    if (src !== currentSrc) {
      this.src = src
      this.state = State.loading
    }
  }

  private renderSrc (next?: Function): void {
    loadImage(this.src).then(() => {
      this.state = State.loaded
      this.render(this.src)
      this.cache.add(this.src)
      next && next()
    }).catch((e) => {
      this.state = State.error
      this.render(this.error)
      warn(`load failed with src image(${this.src}) and the error msg is ${e.message}`)
      next && next()
    })
  }

  private render (src: string): void {
    this.el.setAttribute('src', src)
  }
}
