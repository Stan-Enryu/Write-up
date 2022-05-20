const express = require('express')
const session = require('cookie-session')
const cookieParser = require('cookie-parser')

const app = express()

app.use(express.json({ limit: '2mb' }))
app.use(cookieParser())

app.use(session({
    name: 'session',
    keys: ['5921719c3037662e94250307ec5ed1db']
}))

app.get('/', (req, res) => {
    req.session.username = 'admin'
    res.send({ message: req.cookies })
})

app.listen(80, () => console.log('Listening...'))