'use strict';

/**
 * Dependencies.
 */
var assert = require('assert');
var lupus = require('..');

/**
 * Tests.
 */
describe('lupus()', function() {
  it('should increment the counter 10 times', function(done) {
    var counter = 0;

    lupus(0, 10, function(n) {
      counter++;
    }, function() {
      assert.equal(counter, 10);
      done();
    });
  });

  it('should optionally accept a done callback', function(done) {
    lupus(0, 10, function() {
      done();
    });
  });
});
