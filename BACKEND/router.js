const express = require('express');
const path = require('path');
const fs = require('fs');
const Model = require('./models/Model');
let router = express.Router();

//the video streamer
router.get('/assets/video',(req,res)=>{
    console.log()
    const videoPath = path.join(__dirname,'assets','video.mp4');
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

//respond to xhr of adding user
router.post('/adduser',(req,res)=>{
    console.log(req.body);
    if(req.body == null || req.body == '')
    {
        res.status(400);
        res.send({response:'null body'});
    }
    else if(req.body.name==null || req.body.name=='')
    {
        res.status(400);
        res.send({response:'null name'});
    }
    else if(!req.body.citizenship_no || req.body.citizenship_no=='')
    {
        res.status(400);
        res.send({response:'null citizenship_no'});       
    }
    else if(!req.body.license_no || req.body.license_no=='')
    {
        res.status(400);
        res.send({response:'null license_no'});
    }
    else if(!req.body.address || req.body.address=='')
    {
        res.status(400);
        res.send({response:'null address'});
    }
    else {
        try {
            userCreatePromise= Model.User.create({
                name: req.body.name,
                citizenship_no: req.body.citizenship_no,
                license_no: req.body.license_no,
                address: req.body.address
            });
            userCreatePromise.then((user)=>{
                console.log(`${user} created`);
                res.send({response:'success'});
            },(error)=>{
                console.log(error);
                res.send({response:error});
            });
        }
        catch(e) {
            res.status(400);
            res.send({response: e});
        }
    }
});

// respond to xhr of adding vehicle
router.post('/addvehicle',(req,res)=>{
  console.log(req.body);
  if(req.body == null || req.body == '')
  {
    res.status(400);
    res.send({response:'null body'});
  }
  else if(req.body.licenseNumberInput=='')
  {
     
    res.status(400);
    res.send({response:'null license Number'});
  }
  else if(req.body.owner_ref==null || req.body.owner_ref=='INVALID')
  {
      console.log(req.body.owner_ref);
    res.status(400);
    res.send({response:'null owner'});
  }
  else
  {
      try {
            Model.User.findOne({
                where: {
                    id: req.body.owner_ref
                }
            }).then(user=>
                {
                    Model.Vehicle.create({
                        licensePlateNo: req.body.licensePlateNo,
                        color: req.body.color,
                        typeofVehicle: req.body.typeofVehicle,
                        model: req.body.model
                    }).then(vehicle=>
                        {
                            user.setVehicles([vehicle]);
                            res.send({response:'success'});
                        }, error=>
                        {
                            console.log(error);
                            res.status(400);
                            res.send({response:error});
                        });
                }, error=>
                {
                    console.log(error);
                    res.status(400);
                    res.send({response:error});
                });
        }
      catch(e) {
            res.status(400);
            res.send({response: e});
      }
  }
  
});

//response to xhr of adding infractionrecord


module.exports = router;