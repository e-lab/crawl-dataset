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

	// will take ALOT of time if num=undefined
// google.list({
// 	keyword: userinput,
// 	num: 1000,
// 	rlimit: '2',  // number of requests to Google p second, default: unlimited
// 	setTimeout(function() {}, 10);: 1000,
// 	detail: true,
// 	nightmare: {
// 		show: true
// 	},
//   advanced: {
//     imgType: 'photo', // options: clipart, face, lineart, news, photo
//     resolution: 'm' // options: l(arge), m(edium), i(cons), etc.
//   }
// })

bing.list({
    keyword: userinput,
    num: 100000000000,
 	timeout: 100,
 	detail: true,
 	nightmare: {
 		show: true
 	},
    detail: true
})
.then(function (res) {
	console.log('Results from google', res);

	var json_string = ""

	//converts response json to string
	for(var k = 0; k < res.length; k++) {
		json_string += JSON.stringify(res[k])
		json_string += '\n'
	}

	var fs = require('fs')

    var rootD = "./"+saveFile+"/"
	var dir = rootD + userinput + "/"
	var json_dir = "./json/"

	fs.mkdirSync(dir);
	fs.mkdirSync(json_dir)

	var json_path = json_dir + userinput + "_json.txt"

	//writes json string to file in json folder
	fs.writeFile(json_path, json_string, function (err) {
	  if (err) return console.log(err);
	});

	var downloader = function(i){

		if(i <= res.length){
			console.log('Image number: ', i, '/', res.length)
			var url = res[i-1]['url']
			var path = rootD + userinput + "/" + userinput + i + ".png"

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

					//options to timeout when downloading the image
					var options = {
						url:  url,
					    timeout: 10000
					}
                    // Here may need time out for long downloading time for some images
					request(options, function(err, res, body){
						if(err) {
							console.log('Download timed out...\n')
							downloader(i+1)
						}
					}).pipe(fs.createWriteStream(path)).on('close', function(){
						console.log('Download success')

						gm(path)
						.resize(256)
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
