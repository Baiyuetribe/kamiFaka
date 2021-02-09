"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function loadImage(src) {
    return new Promise(function (resolve, reject) {
        var image = new Image();
        image.onload = function () {
            resolve();
            dispose();
        };
        image.onerror = function (e) {
            reject(e);
            dispose();
        };
        image.src = src;
        function dispose() {
            image.onload = image.onerror = null;
        }
    });
}
exports.default = loadImage;
//# sourceMappingURL=loadImage.js.map