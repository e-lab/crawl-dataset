'use strict'

var EventEmitter = require('events')
  , emitter = new EventEmitter()
	emitter.setMaxListeners(0)

var gm = require('gm')

const jsonFile = process.argv[2]
const imageclass = process.argv[3]

var res = null

var fs = require('fs')
fs.readFile(jsonFile, 'utf8', function(err, data) {
	if (err) throw err;
	console.log('OK: ' + jsonFile);
	//console.log(data)
	res = JSON.parse(data)

	var dic_array = res

	var json_string = ""

	var userinput = imageclass.replace('.txt', '')

	var rootD = "./images/"
	var dir = rootD + userinput + "/"
	var json_dir = dir+"json_"+userinput + "/"

	fs.mkdirSync(dir);
	fs.mkdirSync(json_dir)

	var json_path = json_dir + userinput + "_json.txt"

	var downloader = function(i){

		var success = false
		var cont = true

		if(i <= res.length){
			console.log('Image number: ', i, '/', res.length)
			var url = res[i-1]['url']
	        //I think we need to do something in path 'userinput'
			var path = rootD + userinput + "/" + userinput + i + ".jpeg"

			var fs = require('fs'),
			    request = require('request');

			console.log('Grabbing image info...')

			//sets timeout for retrieving header info
			setTimeout(function() {
				if (success == false) {
					console.log('Timeout while retrieving header info...\n')
					cont = false
					downloader(i+1)
					return
				}
			}, 2000)

			request.head(url, function(err, res, body){
				if (err) {
					//throw err
				} else if (cont == true) {
					success = true
					console.log('image #', i)
					console.log('content-type:', res.headers['content-type'])
					console.log('content-length:', res.headers['content-length'])


					console.log('Downloading image now...')

					//options to timeout when downloading the image
					var options = {
						url:  url,
					    timeout: 300
					}
	                // Here may need time out for long downloading time for some images
					request(options, function(err, res, body){
						if(err) {
							console.log('Download timed out...\n')
							downloader(i+1)
						}
					}).pipe(fs.createWriteStream(path)).on('close', function(){
						console.log('Download success')

						var dic = {url: dic_array[i-1]['url'], path: path}
						json_string += JSON.stringify(dic)
						json_string += '\n'

						//writes json string to file in json folder
						fs.writeFile(json_path, json_string, function (err) {
						  if (err) return console.log(err);
						});

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
});

