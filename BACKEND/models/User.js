const db = require('./sequelize-db');
const Sequelize = require('sequelize');

const User = db.define('user', {
    id: {
        type:Sequelize.BIGINT,
        primaryKey:true,
        autoIncrement:true
    },
    name: Sequelize.STRING,
    address:Sequelize.STRING,
    citizenship_no: {
        type:Sequelize.BIGINT,
        unique:true
    },
    license_no: {
        type:Sequelize.BIGINT,
        unique:true
    }
         
});
module.exports = User;