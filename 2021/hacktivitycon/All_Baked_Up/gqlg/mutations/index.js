const fs = require('fs');
const path = require('path');

module.exports.authenticateUser = fs.readFileSync(path.join(__dirname, 'authenticateUser.gql'), 'utf8');
module.exports.createPost = fs.readFileSync(path.join(__dirname, 'createPost.gql'), 'utf8');
module.exports.createUser = fs.readFileSync(path.join(__dirname, 'createUser.gql'), 'utf8');
