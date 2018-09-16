const http = require('http');
// require the express module
const express = require("express");
// require the body-parser module
const bodyParser = require("body-parser")
const path  = require("path");

// create an object from the express function which we contains methods for making requests and starting the server
const app = express();

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded

// create a route for a GET request to '/' - when that route is reached, run a function
app.get("/", function(req, res) {
  /* inside of this callback we have two large objects, request and response
        request - can contain data about the request (query string, url parameters, form data)
        response - contains useful methods for determining how to respond (with html, text, json, etc.)
    let's respond by sending the text Hello World!
    */
    res.sendFile(path.join(__dirname+'/interface.html'));
    //__dirname : It will resolve to your project folder.
});

app.post('/newmark', function(req, res) {
  var lat = req.body.lat;
  var long = req.body.long;
  console.log(lat);
  console.log(long);
});

// let's tell our server to listen on port 3000 and when the server starts, run a callback function that console.log's a message
app.listen(3000, function() {
  console.log(
    "The server has started on port 3000."
  );
});


/*
const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World\n');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
*/
