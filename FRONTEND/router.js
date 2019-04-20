//the main frontend router
const express = require("express");
let router = express.Router();
const Model = require('../BACKEND/models/Model');

//the add data page handler
router.get('/data',(req,res)=>{

    Model.User.findAll().then((users)=>
    {
        res.render('data',{pageName:'data',users:users});
    },err=>
    {
        res.render('data',{pageName:'data'});
    });
    
  });

//the main page handler
router.get('/',(req,res)=>{
    let currentRows = [[1,"Car", "CL 201 534"],[2,"Car","DL 342 321"],[3, "Bus","Not detected"]];
    let rowsDay = [[1, "CL 201 534", "Car", "Black", "Yes","High"],
                   [2, "CD 231 564", "Bus", "White", "No","Medium"],
                   [3, "MH 234 453","Car","Green","Yes","Low"]];
    res.render('home',{currentRows:currentRows, rowsDay:rowsDay,pageName:"home"});
    
});


module.exports = router;