const Sequelize = require('sequelize');
const sequelize = new Sequelize('major_project', 'ashishthesatan', 'BaaghDactarJeevanRaju', {
  host: 'satandatabase.cvyl8dv21ihz.us-east-1.rds.amazonaws.com',
  dialect: 'postgres',
  
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  },


  // http://docs.sequelizejs.com/manual/tutorial/querying.html#operators
  
});


module.exports = sequelize;