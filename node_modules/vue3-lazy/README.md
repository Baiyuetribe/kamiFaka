# vue3-lazy

## Status: Alpha.

Lazy load plugin for Vue 3.x inspired by [vue-lazyload](https://github.com/hilongjw/vue-lazyload).

This plugin support very simple options, and easy to use.

## Install

```bash
$ npm install vue3-lazy -S
```

## Usage

main.js:

```js
import { createApp } from 'vue'
import App from './app'
import lazyPlugin from 'vue3-lazy'

const app = createApp(App)
lazyPlugin.install(app, {
  loading: 'loading.png',
  error: 'error.png'
})
app.mount('#app')
```

template:

```html
<ul>
  <li v-for="img in list">
    <img v-lazy="img.src" >
  </li>
</ul>
```

## Lazy Options

|key|description|default|options|
|:---|---|---|---|
|`error`|src of the image upon load fail|`'data-src'`|`String`
|`loading`|src of the image while loading|`'data-src'`|`String`|
