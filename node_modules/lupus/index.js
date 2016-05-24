'use strict';


/**
 * This function allows you to safely loop over a range of incrementing integers
 * in an asynchronous fashion.
 *
 * @method
 * @public
 *
 * @param {Integer} start - The number at which to start looping (inclusive).
 * @param {Integer} stop - The number at which to stop looping (exclusive).
 * @param {Function} callback - The callback to run at each iteration of the
 *   loop. The callback should have signature: callback(num) where num is the
 *   integer being processed.
 *  @param {Function} done - The OPTIONAL callback to run once the loop has been
 *    fully iterated over.
 */
module.exports = function(start, stop, callback, done) {
  var task, iterator;
  var current = start;

  iterator = function() {
    if (current >= stop) {
      clearInterval(task);
      if (done) {
        done();
      }
    } else {
      callback(current++);
    }
  }

  task = setInterval(iterator, 0);
};
