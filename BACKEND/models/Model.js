//the main model file that represents the database
const db = require('./sequelize-db');
const Sequelize = require('sequelize');

const User = require('./User');
const Vehicle = require('./Vehicle');
const InfractionRecord = require('./InfractionRecord');

const Op = Sequelize.Op;

//associations
User.hasMany(Vehicle, {
    foreignKey:'owner_ref',
    sourceKey:'id'
});
User.hasMany(InfractionRecord, {
    foreignKey: 'user_ref',
    sourceKey:'id'
})

//to be applied only if db definition is edited... remove in production
db.sync();
module.exports = {
    User: User,
    Vehicle: Vehicle,
    InfractionRecord: InfractionRecord
};