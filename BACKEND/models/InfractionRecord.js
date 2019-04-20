const db = require('./sequelize-db');
const Sequelize = require('sequelize');

const InfractionRecord = db.define('infractionrecord',{
    
    id: { //the partial key: its own id
        type:Sequelize.BIGINT,
        primaryKey:true
    },
    type: { //the type of infraction
        type:Sequelize.ENUM,
        values:['lane infraction','accident','overspeeding','drunk driving','reckless driving'] //todo: to be replaced by enum
        
    },
    severity: {
        type: Sequelize.ENUM,
        values:['mild','moderate','severe','fatal']
        
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
module.exports = InfractionRecord;