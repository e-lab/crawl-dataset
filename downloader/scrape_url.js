'use strict'

var EventEmitter = require('events')
  , emitter = new EventEmitter()
	emitter.setMaxListeners(0)

var Scraper = require ('./index')
//  , google = new Scraper.Google()
    , bing = new Scraper.Bing()

var gm = require('gm')

const userinput = process.argv[2]
const saveFile = process.argv[3]

bing.list({
    keyword: userinput,
    num: 10000,
 	timeout: 100,
 	detail: true,
 	nightmare: {
 		show: true
 	},
    detail: true
})
.then(function (res) {
	console.log('Results from google', res);

	var fs = require('fs');
	fs.writeFile(saveFile, JSON.stringify(res), function(err) {
	    if(err) {
	        return console.log(err);
	    }

	    console.log("The file was saved!");
	}); 

}).catch(function(err) {
	console.log('err',err)
});

