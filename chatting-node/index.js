var app = require('http').createServer(handler)
var io = require('socket.io')(app);
var fs = require('fs');

app.listen(5000);

function handler (req, res) {
  fs.readFile(__dirname + '/index.html',
  function (err, data) {
    if (err) {
      res.writeHead(500);
      return res.end('Error loading ChatMe');
    }
    res.writeHead(200);
    res.end(data);
  });
}

var connections = {};
var groups = {};

io.on('connection', function(socket) {

  // socket.emit('request', /* */); // emit an event to the socket
  // io.emit('broadcast', /* */); // emit an event to all connected sockets

	socket.on('connect', function() {

	});

	socket.on('new-message', function(content) {
		console.log('new message from :' + socket.id);
		socket.broadcast.emit('add-message', content);
	});

	//
	// socket.on('stream', function(image){
	// 	io.sockets.emit('stream', image);
	// });
});
