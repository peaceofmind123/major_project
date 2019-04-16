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
    color: Sequelize.STRING, //TODO: to be replaced by enum
    typeofVehicle:Sequelize.STRING, //TODO: to be replaced by enum
    model: Sequelize.STRING,
    owner_ref: //the reference to the owner (User) of the vehicle 
    {
        type: Sequelize.BIGINT,
        unique:true,
        allowNull:false
    }
});
module.exports = Vehicle;