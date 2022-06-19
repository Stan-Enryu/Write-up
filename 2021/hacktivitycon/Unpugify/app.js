
const express = require('express')
const pug = require('pug')
var bodyParser = require('body-parser');
var path = require('path');

const app = express()
app.set('view engine', 'pug')
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', function (req, res) {
    res.render('index')
})

app.post('/render', function (req, res) {
    template = req.body.template || "h1 No template provided"
    if (blacklist(template) === true) {
        res.status(403)
        res.render('error', {code: 403, error: "You have been Blocked: Forbidden word or symbol detected" })
    } else {
        value = pug.render(template, { pretty: req.body.pretty })
        res.render('render', { value: value})
    }
})

function blacklist(template) {
    var evilwords = ["global","process","mainModule","require","root","child_process","exec","constructor","execSync","spawn","eval","include","new","Function","!","\\","[","]"];
    var arrayLen = evilwords.length;
    for (var i = 0; i < arrayLen; i++) {
        const trigger = template.includes(evilwords[i]);
        if (trigger === true) {
            console.log(evilwords[i])
            return true
        }
    }
}

app.listen(5000)