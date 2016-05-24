# node-lupus

[![NPM Version](https://img.shields.io/npm/v/lupus.svg?style=flat)](https://npmjs.org/package/lupus)
[![NPM Downloads](http://img.shields.io/npm/dm/lupus.svg?style=flat)](https://npmjs.org/package/lupus)
[![Build Status](https://img.shields.io/travis/rdegges/lupus.svg?style=flat)](https://travis-ci.org/rdegges/lupus)

*Async looping for Node.js*

![Banana Peel Sketch](https://github.com/rdegges/node-lupus/raw/master/assets/banana-peel.jpg)


## Meta

- Author: Randall Degges
- Email: r@rdegges.com
- Twitter: [@rdegges](https://twitter.com/rdegges)
- Site: http://www.rdegges.com
- Status: production ready


## Installation

To install `lupus` using [npm](https://www.npmjs.org/), simply run:

```console
$ npm install lupus
```

In the root of your project directory.


## Usage

Once you have `lupus` installed, you can use it to easily iterate over a large
set of numbers asynchronously (*without locking up the CPU!*):

```javascript
var lupus = require('lupus');

lupus(0, 100000, function(n) {
  console.log("We're on:", n);
});
```

Want to run some code after the loop is finished? No problem!

```javascript
var lupus = require('lupus');

lupus(0, 1000000, function(n) {
  console.log("We're on:", n);
}, function() {
  console.log('All done!');
});
```

If you were to try the same thing with a typical for loop, you'd use up a TON of
memory on your computer, as well as block the Node.js process from executing any
other code (*bad*). Don't believe me? Try running the code sample below yourself
=)

```javascript
for (var i = 0; i < 10000000; i++) {
  console.log("We're on:", i);
}

console.log('All done!');
```


## Author's Note

I didn't want to call this library `lupus`, but I didn't really have a choice
since `looper` was already taken! Darn.

I kinda-sorta figured oh well, let's just do this the weird way. Screw it.


## Changelog

v0.0.1: 9-19-2014

    - First release!
