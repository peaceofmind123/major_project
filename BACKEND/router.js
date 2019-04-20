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


// respond to xhr of adding user
router.post('/addvehicle',(req,res)=>{
  console.log(req.body || req.body == '');
  if(req.body == null)
  {
    res.status(400);
    res.send({response:'null body'});
  }
  else if(req.body.licenseNumberInput=='')
  {
     
    res.status(400);
    res.send({response:'null license Number'});
  }
  else if(!req.body.ownerInput || req.body.ownerInput=='INVALID')
  {
    res.status(400);
    res.send({response:'null owner'});
  }
  else
  {
      try {
            vehicle = Model.Vehicle.create(
                {
                    licensePlateNo: req.body.licensePlateNo,
                    color: req.body.color,
                    typeofVehicle: req.body.typeofVehicle,
                    model: req.body.model,
                    owner_ref: req.body.owner_ref
                }
            );
      }
      catch(e) {
            res.status(400);
            res.send({response: e});
      }
  }
  res.send(JSON.stringify({response:"Success!!"}));
});



module.exports = router;