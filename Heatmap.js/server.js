var express = require('express');
var app = express();

var mongoose = require('mongoose');
var mongoosePaginate = require('mongoose-paginate');

var jsonfile = require('jsonfile');
jsonfile.spaces = 4;

var url = 'mongodb://localhost:27017/twitter_db';
mongoose.connect(url);
var Schema = mongoose.Schema;

var tweetSchema = new Schema({
	text: String
},{ collection : 'france_dataset' });

tweetSchema.plugin(mongoosePaginate);

var TwModel = mongoose.model('Tweet', tweetSchema);

// Use connect method to connect to the Server 

app.use(express.static('./public'));

app.get('/', function (req, res) {
	res.sendfile('index.html');
});

var parseTweets = function(docs){
	var locations = []
	for(index in docs){
		tweet = docs[index];
		//tweet = docs[index].toObject();
		if(tweet.coordinates){
			var location = {};
			location.lng = tweet.coordinates.coordinates[0];
			location.lat = tweet.coordinates.coordinates[1];
			location.created_at = tweet.created_at
			locations.push(location);
		}
	}

	return locations;
}

app.get('/SuizavsPolonia',function(req,res){
	var content = jsonfile.readFileSync('./public/files/SuizavsPolonia.json');
	console.log(content)
	res.json(content);
});


app.get('/getTweets', function (req, res) {
	console.log("endpoint /getTweets")
	var query = TwModel.find({}).limit(50000).sort({'_id':1});
  	query.exec(function(err, docs) {
  		if (err) console.log(err);
  		console.log("Test tw france is done")
	  	tweets = parseTweets(docs);
	  	console.log(tweets.length);
  		res.json({tweets:tweets});
	});
});

app.get('/getTweetsPerPage/:page', function (req, res) {
	var page = req.params.page;
	console.log(page);
	var options = {
		sort: { _id: 1 },
    	lean: true,
    	page: page,
    	limit: 2000
	};
	TwModel.paginate({},options)
	.then(function(result) {
		var newpage;
		var docs = result.docs;
		tweets = parseTweets(docs);
		if (tweets.length > 0){
			newpage = parseInt(result.page) + 1;
		}else{
			newpage = -1;
		}
		res.json({ 'tweets': tweets , 'page': newpage });
	});
});

var server = app.listen(4060, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Heatmap Application listening at http://%s:%s', host, port);
});

