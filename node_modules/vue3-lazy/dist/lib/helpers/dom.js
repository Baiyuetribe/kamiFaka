"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var inBrowser = typeof window !== 'undefined';
exports.hasIntersectionObserver = checkIntersectionObserver();
function checkIntersectionObserver() {
    if (inBrowser &&
        'IntersectionObserver' in window &&
        'IntersectionObserverEntry' in window &&
        'intersectionRatio' in IntersectionObserverEntry.prototype) {
        // Minimal polyfill for Edge 15's lack of `isIntersecting`
        // See: https://github.com/w3c/IntersectionObserver/issues/211
        if (!('isIntersecting' in IntersectionObserverEntry.prototype)) {
            Object.defineProperty(IntersectionObserverEntry.prototype, 'isIntersecting', {
                get: function () {
                    return this.intersectionRatio > 0;
                }
            });
        }
        return true;
    }
    return false;
}
var style = function (el, prop) {
    return getComputedStyle(el).getPropertyValue(prop);
};
var overflow = function (el) {
    return style(el, 'overflow') + style(el, 'overflow-y') + style(el, 'overflow-x');
};
function scrollParent(el) {
    var parent = el;
    while (parent) {
        if (parent === document.body || parent === document.documentElement) {
            break;
        }
        if (!parent.parentNode) {
            break;
        }
        if (/(scroll|auto)/.test(overflow(parent))) {
            return parent;
        }
        parent = parent.parentNode;
    }
    return window;
}
exports.scrollParent = scrollParent;
//# sourceMappingURL=dom.js.map