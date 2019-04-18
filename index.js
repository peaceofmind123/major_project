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
const path = require('path');
const Model = require(path.join(__dirname,'BACKEND','models','Model'));
app.engine('handlebars',handleBars({defaultLayout:'main',
                                    layoutsDir:path.join(__dirname,'BACKEND','views','layouts'),
                                    helpers:{
                                      ifequals: function(obj1, obj2,options) {
                                        if(obj1==obj2)
                                          return options.fn(this);
                                        else
                                          return options.inverse(this); 
                                      }
                                    }}));
app.set('view engine','handlebars');
app.set('views',path.join(__dirname,'BACKEND','views'));
app.use(express.static(path.join(__dirname,'BACKEND','public')));
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
    let currentRows = [[1,"Car", "CL 201 534"],[2,"Car","DL 342 321"],[3, "Bus","Not detected"]];
    let rowsDay = [[1, "CL 201 534", "Car", "Black", "Yes","High"],
                   [2, "CD 231 564", "Bus", "White", "No","Medium"],
                   [3, "MH 234 453","Car","Green","Yes","Low"]];
    res.render('home',{currentRows:currentRows, rowsDay:rowsDay,pageName:"home"});
    
});
app.get('/assets/video',(req,res)=>{
  const videoPath = path.join(__dirname,'BACKEND','assets','video.mp4');
  const stat = fs.statSync(videoPath);
  const fileSize = stat.size;
  const range = req.headers.range;
  if (range) {
    const parts = range.replace(/bytes=/, "").split("-");
    const start = parseInt(parts[0], 10);
    const end = parts[1]
      ? parseInt(parts[1], 10)
      : fileSize-1;
    const chunksize = (end-start)+1;
    const file = fs.createReadStream(videoPath, {start, end});
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
    fs.createReadStream(videoPath).pipe(res);
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