#!/usr/bin/env node
console.log("Hello " + process.argv[2] + "!");  

const typedArray = new Uint8Array([1, 2, 3, 4]);
const normalArray = Array.from(typedArray);

const arrayBuffer = typedArray.buffer;

console.log(arrayBuffer)
console.log(new Uint8Array(arrayBuffer))


let buffer = Buffer.from(arrayBuffer);


console.log(buffer,buffer.length,buffer.length,buffer.toString())

const fs  = require('fs');

// fs.appendFileSync('test.buffer', buffer);

var path ='./test.buffer'
fs.open(path, 'w', function(err, fd) {
    if (err) {
        throw 'could not open file: ' + err;
    }

    // write the contents of the buffer, from position 0 to the end, to the file descriptor returned in opening our file
    fs.write(fd, buffer, 0, buffer.length, null, function(err) {
        if (err) throw 'error writing file: ' + err;
        fs.close(fd, function() {
            console.log('wrote the file successfully');
        });
    });
});



fs.readFile(path, function (err, data) {
    if (err) throw err;
    console.log(new Uint8Array(data));
});