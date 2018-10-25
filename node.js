var mysql = require('mysql');
var http = require('http');
//var nodemailer = require('nodemailer');


var connection = mysql.createConnection({
    host     : 'academic-mysql.cc.gatech.edu',
    user     : 'cs4400_group32',
    password : 'AXtzKclB',
    database : 'cs4400_group32'
});

connection.connect();

connection.query('select * from `User`', function (error, results, fields) {
    if (error) {
        console.log(err.code);
        console.log(err.fatal);
    }
    console.log('The solution is: ', results);
});



http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    
}).listen(8080);



//var transporter = nodemailer.createTransport({
//  service: 'gmail',
 // auth: {
//    user: 'luohaozh@msu.edu',
//    pass: 'Lucky@2018'
//  }
//});

//var mailOptions = {
//  from: 'youremail@gmail.com',
 // to: 'myfriend@yahoo.com',
  //subject: 'Sending Email using Node.js',
  //text: 'That was easy!'
//};

//transporter.sendMail(mailOptions, function(error, info){
  //if (error) {
    //console.log(error);
  //} else {
    //console.log('Email sent: ' + info.response);
  //}
//});


//var crypto = require('crypto');
//var name = 'braitsch';
//var hash = crypto.createHash('md5').update(name).digest('hex');
//console.log(hash); // 9b74c9897bac770ffc029102a200c5de
