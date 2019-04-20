const db = require('./sequelize-db');
const Sequelize = require('sequelize');

const Vehicle = db.define('vehicle',{
    id: {
        type: Sequelize.BIGINT,
        primaryKey:true,
        autoIncrement:true
    },
    licensePlateNo: {
        type: Sequelize.STRING,
        unique: true
    },
    color: {
        type: Sequelize.ENUM,
        values: ['black','blue','red','green','purple','yellow','brown','white']}, 
    typeofVehicle:{
        type:Sequelize.STRING,
        values:['car','bus','truck','scooter','motorbike','moped','SUV','van']
    }, 
    model: Sequelize.STRING
    
});
module.exports = Vehicle;