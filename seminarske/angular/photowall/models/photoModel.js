var mongoose = require('mongoose');
var Schema   = mongoose.Schema;

var photoSchema = new Schema({
	'name' : String,
	'path' : String,
	'views' : { type: Number, default: 0 },
	'likes' : { type: Number, default: 0 }
});

module.exports = mongoose.model('photo', photoSchema);
