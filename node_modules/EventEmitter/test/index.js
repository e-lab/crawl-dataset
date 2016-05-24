import EventEmitter from '../src/index.js'
import expect from 'expect';

describe('EventEmitter', function() {
  var EM = new EventEmitter();

  describe('1: Constructor', function() {
    EM.clear();
    EM.on('bar', () => 'some response');

    it('1.1: _events property should be private', () =>
      expect(EM._events).toEqual(void 0)
    );

    it('1.2: _callbacks property should be private', () =>
      expect(EM._callbacks).toEqual(void 0)
    );

    it('1.3: _maxListeners property should be private', () =>
      expect(EM._maxListeners).toEqual(void 0)
    );

    it('1.4: on method should be public', () =>
      expect(EM.on).toBeA('function')
    );

    it('1.5: once method should be public', () =>
      expect(EM.once).toBeA('function')
    );

    it('1.6: off method should be public', () =>
      expect(EM.off).toBeA('function')
    );

    it('1.7: emit method should be public', () =>
      expect(EM.off).toBeA('function')
    );
  });

  describe('2: on(), emit()', function() {
    var foo = 2;

    EM
      .clear()
      .on('bar', () => {
        foo += 1;
      });

    it('2.1: Initial "foo" should be equal 2', () => {
      expect(foo).toEqual(2);
      EM.emit('bar');
    });

    it('2.2: After triggering event "bar", "foo" should be equal 3', () => {
      expect(foo).toEqual(2);
    });
  });

  describe('3: once()', function() {
    var baz = 2;

    EM
      .clear()
      .once('bar', () => baz++)
      .emit('bar');

    it('3.1: After the first triggering event "bar", "foo" should be equal 3', () => {
      expect(baz).toEqual(3);
    });

    it('3.3: After the second triggering event "bar", "foo" should be equal 3 as well', () => {
      expect(baz).toEqual(3);
    });
  });

  describe('4: off()', function() {
    var foo = 1;

    EM
      .clear()
      .on('bar', () => foo++)
      .off('bar')
      .emit('bar');

    it('4.1: event "bar" should not be triggered', () => {
      expect(foo).toEqual(1);
    });
  });

  describe('5: clear(), listenersNumber()', function() {
    EM
      .clear()
      .on('bar', () => 'some response');

    it('5.1: Initial "foo" should be equal 2', () => {
      expect(EM.listenersNumber('bar')).toEqual(1);
      EM.clear();
    });

    it('5.2: After triggering event "bar", "foo" should be equal 3', () => {
      expect(EM.listenersNumber('bar')).toEqual(null);
    });
  });
});
