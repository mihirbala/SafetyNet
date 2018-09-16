var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var express = require('express');
const bodyParser = require("body-parser")
const path  = require("path");

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded
app.use(express.static('templates'));

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
});

// create a route for a GET request to '/' - when that route is reached, run a function
app.get("/", function(req, res) {
    res.sendFile(path.join(__dirname+'/templates/main.html'));
    //__dirname resolves to project folder.
});

app.post('/newmark', function(req, res) {
  var lat = req.body.lat;
  var lng = req.body.lng;
  var img = req.body.img;
  io.emit('new coords', {'lat' : lat, 'lng' : lng, 'img' : img});
  res.send("Added point of interest!");
});

// tell server to listen on port 3000 and when the server starts, run a callback function that console.log's a message
http.listen(3000, function() {
  console.log(
    "The server has started on port 3000."
  );
});
