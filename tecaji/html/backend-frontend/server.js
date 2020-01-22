var http = require('http');
var fs = require('fs');

http.createServer(function (req, res) {

  if(req.url == "/"){
    res.writeHead(200, {'Content-Type': 'text/html'});
    var index = fs.readFileSync('frontend.html', 'utf-8');
    res.write(index);
  }

  if(req.url == "/database" ){
    res.writeHead(200, {'Content-Type': 'text/plain'});

    var fileContent = fs.readFileSync('database.txt', 'utf-8');

    res.write(fileContent);
  }

  if(req.url.includes("/database/" )){
    res.writeHead(200, {'Content-Type': 'text/html'});
    fs.appendFileSync('database.txt', req.url + '\n', 'utf-8')
    res.write("<h1>I get your message ;)</h1>");
  }

  res.end();

}).listen(8080);