const db = require('./sequelize-db');
const Sequelize = require('sequelize');

const InfractionRecord = db.define('infractionrecord',{
    user_ref: //the reference to the user that this record pertains to
    {
        type: Sequelize.BIGINT,
        primaryKey:true 
    },
    id: { //the partial key: its own id
        type:Sequelize.BIGINT,
        primaryKey:true
    },
    type: { //the type of infraction
        type:Sequelize.STRING, //todo: to be replaced by enum
        
    },
    severity: {
        type: Sequelize.STRING, //todo: to be replaced by enum
        
    },
    date: {
        type:Sequelize.DATE
    },
    time: {
        type: Sequelize.TIME
    },
    location: {
        type: Sequelize.STRING
    }
});