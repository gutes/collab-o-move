var app = require('express').createServer()
   ,io = require('socket.io').listen(app)
   ,zmq =  require('zmq')
   ,sock = zmq.socket('push');


sock.bindSync('tcp://10.0.0.22:3000');

app.listen(8080);

app.get('/', function (req, res) {
  res.sendfile(__dirname + '/event_test.html');
});

io.set('log level', 1);
io.sockets.on('connection', function (socket) {
	
  socket.on('devicemotion', function (data) {
	
	//console.log( data );

	sock.send( JSON.stringify(data) );
	
  });
});