import { DirectiveBinding } from 'vue'
import { LazyOptions, State, Target } from '../types'
import { hasIntersectionObserver, scrollParent } from '../helpers/dom'
import ImageManager from './imageManager'
import { throttle } from '../helpers/util'

const DEFAULT_URL = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'

const events = ['scroll', 'wheel', 'mousewheel', 'resize', 'animationend', 'transitionend', 'touchmove', 'transitioncancel']

const THROTTLE_DELAY = 300

export default class Lazy {
  error: string
  loading: string
  cache: Set<string>
  managerQueue: ImageManager[]
  observer?: IntersectionObserver
  targetQueue?: Target[]
  throttleLazyHandler: Function

  constructor (options: LazyOptions) {
    this.error = options.error || DEFAULT_URL
    this.loading = options.loading || DEFAULT_URL

    this.cache = new Set()
    this.managerQueue = []
    this.throttleLazyHandler = throttle(this.lazyHandler.bind(this), THROTTLE_DELAY)

    this.init()
  }

  add (el: HTMLElement, binding: DirectiveBinding): void {
    const src = binding.value
    const parent = scrollParent(el)

    const manager = new ImageManager({
      el,
      parent,
      src,
      error: this.error,
      loading: this.loading,
      cache: this.cache
    })

    this.managerQueue.push(manager)

    if (hasIntersectionObserver) {
      this.observer!.observe(el)
    } else {
      this.addListenerTarget(parent)
      this.addListenerTarget(window)
      this.throttleLazyHandler()
    }
  }

  update (el: HTMLElement, binding: DirectiveBinding): void {
    const src = binding.value
    const manager = this.managerQueue.find((manager) => {
      return manager.el === el
    })
    if (manager) {
      manager.update(src)
    }
  }

  remove (el: HTMLElement): void {
    const manager = this.managerQueue.find((manager) => {
      return manager.el === el
    })
    if (manager) {
      this.removeManager(manager)
    }
  }

  private init (): void {
    if (hasIntersectionObserver) {
      this.initIntersectionObserver()
    } else {
      this.targetQueue = []
    }
  }

  private initIntersectionObserver (): void {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const manager = this.managerQueue.find((manager) => {
            return manager.el === entry.target
          })
          if (manager) {
            if (manager.state === State.loaded) {
              this.removeManager(manager)
              return
            }
            manager.load()
          }
        }
      })
    }, {
      rootMargin: '0px',
      threshold: 0
    })
  }

  private addListenerTarget (el: HTMLElement | Window): void {
    let target = this.targetQueue!.find((target) => {
      return target.el === el
    })

    if (!target) {
      target = {
        el,
        ref: 1
      }
      this.targetQueue!.push(target)
      this.addListener(el)
    } else {
      target.ref++
    }
  }

  private removeListenerTarget (el: HTMLElement | Window): void {
    this.targetQueue!.some((target, index) => {
      if (el === target.el) {
        target.ref--
        if (!target.ref) {
          this.removeListener(el)
          this.targetQueue!.splice(index, 1)
        }
        return true
      }
      return false
    })
  }

  private addListener (el: HTMLElement | Window): void {
    events.forEach((event) => {
      el.addEventListener(event, this.throttleLazyHandler as EventListenerOrEventListenerObject, {
        passive: true,
        capture: false
      })
    })
  }

  private removeListener (el: HTMLElement | Window): void {
    events.forEach((event) => {
      el.removeEventListener(event, this.throttleLazyHandler as EventListenerOrEventListenerObject)
    })
  }

  private lazyHandler (e: Event): void {
    for (let i = this.managerQueue.length - 1; i >= 0; i--) {
      const manager = this.managerQueue[i]
      if (manager.isInView()) {
        if (manager.state === State.loaded) {
          this.removeManager(manager)
          return
        }
        manager.load()
      }
    }
  }

  private removeManager (manager: ImageManager): void {
    const index = this.managerQueue.indexOf(manager)
    if (index > -1) {
      this.managerQueue.splice(index, 1)
    }
    if (this.observer) {
      this.observer.unobserve(manager.el)
    } else {
      this.removeListenerTarget(manager.parent)
      this.removeListenerTarget(window)
    }
  }
}
