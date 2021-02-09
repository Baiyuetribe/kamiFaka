"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var lazy_1 = require("./core/lazy");
var lazyPlugin = {
    install: function (app, options) {
        var lazy = new lazy_1.default(options);
        app.directive('lazy', {
            mounted: lazy.add.bind(lazy),
            updated: lazy.update.bind(lazy),
            unmounted: lazy.update.bind(lazy)
        });
    }
};
exports.default = lazyPlugin;
//# sourceMappingURL=index.js.map