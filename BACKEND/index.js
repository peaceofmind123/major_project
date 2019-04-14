const express = require('express');
const app = express();
const PORT = process.env.PORT || 8000;
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const debug = require('debug');
const session = require('express-session');
const handleBars = require('express-handlebars');
const morgan = require('morgan');

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