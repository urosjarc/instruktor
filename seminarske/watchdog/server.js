const express = require('express');
const app = express();
const port = 3000;
const watchdog = require('./watchdog');

process.on("exit", function(code) {
    console.error("============================ EXIT EVENT");
    console.log("Detecting exit event: " + code);
    if(code === 3){
        console.log("Restarting & resetting application...");
        require("child_process").spawn(process.argv.shift(), process.argv, {
            cwd: process.cwd(),
            detached : true,
            stdio: "inherit"
        });
    }
    console.error("============================ END EXIT EVENT");
});

const info = {
    startedAt: new Date(),
    runningTime: 0,
    reqIndex: 0,
    uniqueIPS: [],
    reqHistory: { }
};

app.get('/diagnostika', (req, res) => {

    const now = new Date();

    info.reqIndex++;
    info.runningTime = (now - info.startedAt)/1000;
    info.reqHistory[now] = {
        IP: req.ip,
        QUERY: req.url
    };

    if(info.uniqueIPS.indexOf(req.ip) === -1)
        info.uniqueIPS.push(req.ip);

    if(req.query.password !== "pass")
        res.send(`
            <h1>Geslo je napacno: <u>${req.query.password}</u></h1>
            <h3>/diagnostika?password=${req.query.password}&endless=${req.query.endless}</h3>`);
    else {
        watchdog(req.query.endless==='true');
        res.send(info);
    }
});

app.listen(port, () => {
    console.log(`Listening at http://localhost:${port}`)
});