const express = require('express');
const app = express();
const PORT = process.env.PORT || 8000;
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const debug = require('debug');
const session = require('express-session');
const handleBars = require('express-handlebars');
const morgan = require('morgan');
const fs = require('fs');
app.engine('handlebars',handleBars({defaultLayout:'main'}));
app.set('view engine','handlebars');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(session({
    secret:'baagh_dactar_jeevan_raju',
    saveUninitialized:true,
    resave:true
}));
app.use(morgan('tiny'));


app.get('/',(req,res)=>{
    console.log('request recieved!!');
    res.render('home');
    
});
app.get('/assets/video',(req,res)=>{
  const path = 'assets/video.mkv';
  const stat = fs.statSync(path);
  const fileSize = stat.size;
  const range = req.headers.range;
  if (range) {
    const parts = range.replace(/bytes=/, "").split("-");
    const start = parseInt(parts[0], 10);
    const end = parts[1]
      ? parseInt(parts[1], 10)
      : fileSize-1;
    const chunksize = (end-start)+1;
    const file = fs.createReadStream(path, {start, end});
    const head = {
      'Content-Range': `bytes ${start}-${end}/${fileSize}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': 'video/mp4',
    };
    res.writeHead(206, head);
    file.pipe(res);
  } else {
    const head = {
      'Content-Length': fileSize,
      'Content-Type': 'video/mp4',
    };
    res.writeHead(200, head);
    fs.createReadStream(path).pipe(res);
  }
});
//404 handler
app.use((req,res,next)=>{
    //TODO: render 404 page here
    console.log('page not found: '+req.url);
    next();
});
//500 handler
app.use((err,req,res,next)=>{
    //TODO: render 500 page here
    next();
});
app.listen(PORT,()=>{
    debug(`Server listening on port ${PORT}`);
});