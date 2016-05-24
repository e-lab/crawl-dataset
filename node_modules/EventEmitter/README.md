
# EventEmitter in JavaScript

## Synopsis

EventEmitter is an implementation of the Event-based architecture in JavaScript.

The code is written using the ES2015 approaches, including creation of private property through WeakMap that allows you to not to check for clearing memory, and let it do to the garbage collector.

The module contains the most basic and necessary things: subscription to an event, unsubscribing from the events, running event only once, setting the maximum number of listeners.

The focus is on code readability, speed of execution, getting rid of all the excess.

You can use this library in browser either at the server as within the node.js.

## Dependencies

There are no dependencies. You need only npm installed and just run `npm install` to grab the development dependencies.

## Examples

```javascript
  let EM = new EventEmitter();

  EM.on('foo', () => {
    // some code...
  });

  EM.emit('foo');
```

```javascript
  let EM = new EventEmitter();

  EM.once('foo', () => {
    // some code...
  });

  EM.emit('foo');
```

```javascript
  let EM = new EventEmitter();

  EM.once('foo', (bar, baz) => {
    // some code...
  });

  EM.emit('foo', 'var 1 for bar', 'var 2 for baz');
```

```javascript
  let EM = new EventEmitter();

  EM.on('foo', () => {
    // some code...
  });

  // Note: you can use chaining.
  EM
    .emit('foo')
    .emit('foo')
    .off('foo');
```

```javascript
  // You can set maxNumberOfListeners as a parameter when creating new object.
  let EM = new EventEmitter(1);

  EM.on('foo', () => {
    // some code...
  });
  // Note: it will show notification in console.
  EM.on('foo', () => {
    // some other code...
  });
```

## Testing

Tests are performed using mocha and expect library.

## Building the documentation

You can use JSDoc comments found within the source code.

## Minifying

You can grab minified versions of EventEmitter from /dist path after running `gulp build`.

## Todo

1. Add event's namespace:

```javascript
  EM.on('foo.*', () => {
    // some code...
  });
```

2. Add events through comma:

```javascript
  EM.on('foo,bar,baz', () => {
    // some code...
  });
```

3. Add method "onAny" for listening each event:

```javascript
  EM.onAny(() => {
    // some code...
  });
```
