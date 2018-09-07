#!/usr/bin/env node
const express = require('express');
const http = require('http');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.text({
    type: function(req) {
        return 'text';
    }
}));

app.post('/', function (req, res) {
    console.log(req.body);
    res = res.status(200);
    if (req.get('Content-Type')) {
        console.log("Content-Type: " + req.get('Content-Type'));
        res = res.type(req.get('Content-Type'));
    }
    res.send(req.body);
});

const port = process.argv[2];
http.createServer(app).listen(port);
console.log(`Port: ${port}`);

// This is a simple echo server for now.
