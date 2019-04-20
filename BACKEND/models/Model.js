//the main model file that represents the database
const db = require('./sequelize-db');
const Sequelize = require('sequelize');

const User = require('./User');
const Vehicle = require('./Vehicle');
const InfractionRecord = require('./InfractionRecord');

const Op = Sequelize.Op;

//associations
User.hasMany(Vehicle);

User.hasMany(InfractionRecord);

//to be applied only if db definition is edited... remove in production
//db.sync();
module.exports = {
    User: User,
    Vehicle: Vehicle,
    InfractionRecord: InfractionRecord
};