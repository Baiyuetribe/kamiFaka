export function throttle (fn: Function, delay: number): Function {
  let timeout = 0
  let lastRun = 0
  return function (this: void) {
    if (timeout) {
      return
    }
    const elapsed = Date.now() - lastRun
    const context = this
    const args = arguments
    const runCallback = function () {
      lastRun = Date.now()
      timeout = 0
      fn.apply(context, args)
    }
    if (elapsed >= delay) {
      runCallback()
    } else {
      timeout = window.setTimeout(runCallback, delay)
    }
  }
}
