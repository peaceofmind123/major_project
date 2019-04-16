const Sequelize = require('sequelize');
const sequelize = new Sequelize('major-project', 'postgres', 'baaghdactarjeevanraju', {
  host: 'localhost',
  dialect: 'postgres',

  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  },


  // http://docs.sequelizejs.com/manual/tutorial/querying.html#operators
  operatorsAliases: false
});


module.exports = sequelize;