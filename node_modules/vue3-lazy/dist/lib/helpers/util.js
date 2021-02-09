"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function throttle(fn, delay) {
    var timeout = 0;
    var lastRun = 0;
    return function () {
        if (timeout) {
            return;
        }
        var elapsed = Date.now() - lastRun;
        var context = this;
        var args = arguments;
        var runCallback = function () {
            lastRun = Date.now();
            timeout = 0;
            fn.apply(context, args);
        };
        if (elapsed >= delay) {
            runCallback();
        }
        else {
            timeout = window.setTimeout(runCallback, delay);
        }
    };
}
exports.throttle = throttle;
//# sourceMappingURL=util.js.map