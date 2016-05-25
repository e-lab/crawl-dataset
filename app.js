'use strict'

var EventEmitter = require('events')
  , emitter = new EventEmitter()
	emitter.setMaxListeners(0)

var Scraper = require ('./index')
  , google = new Scraper.Google()

var gm = require('gm')

function getKeyword(callback){

	var readline = require('readline')

	var rl = readline.createInterface({
	  input: process.stdin,
	  output: process.stdout
	});

	rl.question('Enter image search keyword: ', (userinput) => {
	  callback(userinput)
	  rl.close();
	});
}

getKeyword(function(userinput){
	// will take ALOT of time if num=undefined
	google.list({
		keyword: userinput,
		num: 1000,
		rlimit: '2',  // number of requests to Google p second, default: unlimited
    	timeout: 10000,
		detail: true,
		nightmare: {
			show: true
		},
	  advanced: {
	    imgType: 'photo', // options: clipart, face, lineart, news, photo
	    resolution: 'm' // options: l(arge), m(edium), i(cons), etc.
	  }
	})
	.then(function (res) {
		console.log('Results from google', res);

		var downloader = function(i){
			if(i <= res.length){
				console.log('Image number: ', i, '/', res.length)
				var url = res[i-1]['url']
				var path = "./images/" + userinput + i + ".png"

				var fs = require('fs'),
				    request = require('request');

				console.log('Grabbing image info...')

				request.head(url, function(err, res, body){
					if (err) {
						//throw err
						downloader(i+1)
					} else {
						console.log('content-type:', res.headers['content-type'])
						console.log('content-length:', res.headers['content-length'])


						console.log('Downloading image now...')

						request(url).pipe(fs.createWriteStream(path)).on('close', function(){
							console.log('Download success')

							gm(path)
							.resize(400)
							.write(path, function (err) {
							  if (!err){
							  	console.log('Image has been resized\n');
							  } else {
							  	console.log('err', err)
							  }

							  downloader(i+1)
							  
							});
						});
					}
				}).on('error', function (err) { 
					console.log('err',err)
				});
			}
		}

		downloader(1)
		
	}).catch(function(err) {
		console.log('err',err)
	});
})

// var Scraper = require ('images-scraper')
//   , bing = new Scraper.Bing();

// bing.list({
//     keyword: 'banana',
//     num: 10,
//     detail: true
// })

// yahoo.list({
//     keyword: 'banana',
//     num: 10,
// }).then(function (res) {
//     console.log('results', res);
// }).catch(function (err) {
//     console.log('err',err);
// });

// pics.list({
//     keyword: 'banana',
//     num: 10,
// }).then(function (res) {
//     console.log('out',res);
// }).catch(function (err) {
//     console.log('err',err);
// });