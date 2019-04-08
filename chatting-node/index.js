var http = require('http');
var app = http.createServer(handler)
var io = require('socket.io')(app);
var fs = require('fs');
var querystring = require('querystring');
var sync_request = require('sync-request');
var request = require('request');

const TOKEN = getToken('chatting_node', 'chatmeee');

app.listen(5000, "0.0.0.0");

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

function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] === value);
}

var connections = {};
var groups = {};
var allClients = [];

// middleware
io.use((socket, next) => {
  let token = socket.handshake.query.token;
	let user_id = socket.handshake.query.user_id;
  if (syncValidateUser(token, user_id)) {
		connections[socket.id] = user_id;
    return next();
  }
  return next(new Error('authentication error'));
});


io.on('connection', function(socket) {
	request.get(
		'http://localhost:8000/api/group',
		{
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Token ' + TOKEN
			}
		}, function (error, response, body) {
			if (!error && response.statusCode == 200) {
				var obj = JSON.parse(body);
				for (var i = 0; i < obj.length; i++) {
					var group = obj[i];
					if (group['users'].indexOf(Number(connections[socket.id])) >= 0 ) {
						socket.join(group['name']);
					}
				}
			}
		}
	);

	socket.on('disconnect', function() {
		delete connections[socket.id];
	});

	socket.on('new-message', function(content) {
		content.sender = connections[socket.id];
		request.post(
	    'http://localhost:8000/api/chat/',
	    {
				json: content,
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Token ' + TOKEN
		  	}
			},
	    function (error, response, body) {
	      if (!error && response.statusCode == 201) {
					var message = body;
					console.log(message);
					message.receiver = message.receiver + '';
					console.log(connections);
					if (message.type == 'S') { //single user
						if (getKeyByValue(connections, message.receiver) != undefined) {
							io.to(getKeyByValue(connections, message.receiver)).emit('add-message', message);
						}
						socket.emit('add-message', message);
					} else if (message.type == 'G') { //group
						io.to(message['group_name']).emit('add-message', message);
					} else if (message.type == 'A') { //server
						io.sockets.emit('add-message', message);
					}
	      }
	    }
		);
	});

	setInterval(() => {
		var values = Object.keys(connections).map(function(key){
    	return connections[key];
		});
		socket.emit('refresh-connected-users', values);
	}, 3000);

});


function syncValidateUser(_token, _user_id) {
	var res = sync_request('POST', 'http://localhost:8000/api/validate-token/', {
	  json: { user_id: _user_id, token: _token },
		headers: {
			'Content-Type': 'application/json',
			'Authorization': 'Token ' + TOKEN
  	}
	});
	var res = JSON.parse(res.getBody('utf8'));
	return res['valid'];
}

function getToken(user_name, password) {
	var res = sync_request('POST', 'http://localhost:8000/get-token/', {
	  json: { username: user_name, password: password },
		headers: {
			'Content-Type': 'application/json'
  	}
	});
	var res = JSON.parse(res.getBody('utf8'));
	return res['token'];
}
