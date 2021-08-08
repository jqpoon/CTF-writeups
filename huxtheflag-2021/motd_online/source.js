const e = require('express'); 
const express = require('express'); 
var http = require('http'); 
const secrets = require("./secret"); 
var Mustache = require('mustache'); 
const fs = require('fs') 
const app = express(); 
const port = 3000; 

isObject = function(a) { return (!!a) && (a.constructor === Object); }; 

app.get('/api/motd', (req, res) => { 
    res.send('This too shall pass...'); 
}) 

app.get('/displaysource', (req, res) => { 
    fs.readFile('server.js', 'utf8' , (err, data) => { 
        if (err) { 
            console.error(err) 
            return 
        } 
        res.send(data); 
    }); 
}) 

app.get('/admin', (req, res) => { 
    if (req.ip != '::ffff:127.0.0.1') { 
        res.send('This page is only for admins with local access!'); 
    } else { 
        res.send(secrets.flag); 
    } 
}) 

app.get('/', (req, res) => { 
    var userOpts = { "theme": "light", "is_debug": false, "greeting": "Guest" }; 

    try { 
        var newOpts = JSON.parse(req.query.userOpts); 
        
        for (var key in newOpts) { 
            if (key == "theme" && newOpts[key] != "light" && newOpts[key] != "dark") { 
                continue; 
            } 

            if (key == "is_debug" && typeof newOpts[key] != "boolean") { 
                continue; 
            } 

            if (key == "greeting") { 
                if (typeof newOpts[key] != "string") { 
                    continue; 
                } 
                newOpts[key].replace(/\W/g, ''); 
            } 

            if (isObject(newOpts[key])) { 
                for (var k in newOpts[key]) { 
                    userOpts[key][k] = newOpts[key][k]; 
                } 
            } else { 
                userOpts[key] = newOpts[key]; 
            } 
        } 
    } catch (error) { 

} 

var reqOpts = { host: '127.0.0.1', port: '3000', }; // support for custom paths in the future 

if (reqOpts['path'] == undefined) { 
    reqOpts['path'] = '/api/motd'; 
}

var req = http.get(reqOpts, function(res1) { 
    var bodyChunks = []; 
    res1.on('data', function(chunk) { bodyChunks.push(chunk); })
        .on('end', function() { 
            var body = Buffer.concat(bodyChunks); 
            fs.readFile('template.html', 'utf8' , (err, data) => { 
                if (err) { 
                    console.error(err) 
                    return 
                } 
            res.send(Mustache.render(data, {data: body, greet: userOpts.greeting, theme: userOpts["theme"]})); 
            });
        }); 
    }); 
}) 

app.listen(port, () => { console.log(`Example app listening at http://localhost:${port}`) })


https://blog.0daylabs.com/2019/02/15/prototype-pollution-javascript/
https://book.hacktricks.xyz/pentesting-web/deserialization/nodejs-proto-prototype-pollution