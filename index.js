//const declarations
const PORT = process.env.PORT || 8000;

//const imports
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const debug = require('debug');
const session = require('express-session');
const handleBars = require('express-handlebars');
const morgan = require('morgan');

const path = require('path');

const frontendRouter = require('./FRONTEND/router');
const backendRouter = require('./BACKEND/router');

//application setup
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
app.use('/api',backendRouter);
app.use('/',frontendRouter);

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