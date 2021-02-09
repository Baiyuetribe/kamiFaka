const inBrowser = typeof window !== 'undefined'

export const hasIntersectionObserver = checkIntersectionObserver()

function checkIntersectionObserver (): boolean {
  if (inBrowser &&
    'IntersectionObserver' in window &&
    'IntersectionObserverEntry' in window &&
    'intersectionRatio' in IntersectionObserverEntry.prototype) {
    // Minimal polyfill for Edge 15's lack of `isIntersecting`
    // See: https://github.com/w3c/IntersectionObserver/issues/211
    if (!('isIntersecting' in IntersectionObserverEntry.prototype)) {
      Object.defineProperty(IntersectionObserverEntry.prototype,
        'isIntersecting', {
          get: function (this: IntersectionObserverEntry) {
            return this.intersectionRatio > 0
          }
        })
    }
    return true
  }
  return false
}

const style = (el: HTMLElement, prop: string): string => {
  return getComputedStyle(el).getPropertyValue(prop)
}

const overflow = (el: HTMLElement): string => {
  return style(el, 'overflow') + style(el, 'overflow-y') + style(el, 'overflow-x')
}

export function scrollParent (el: HTMLElement): HTMLElement | Window {
  let parent = el

  while (parent) {
    if (parent === document.body || parent === document.documentElement) {
      break
    }

    if (!parent.parentNode) {
      break
    }

    if (/(scroll|auto)/.test(overflow(parent))) {
      return parent
    }

    parent = parent.parentNode as HTMLElement
  }

  return window
}
