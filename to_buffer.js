// node ./to_buffer {a,b,c,d} ./where/to/save

// console.log(process.argv);

const data = process.argv[2];
const loc = process.argv[3];

const typedArray = new Uint16Array(eval(data));
const arrayBuffer = typedArray.buffer;
const buffer = Buffer.from(arrayBuffer);

const fs  = require('fs')

fs.open(loc, 'w', function(err, fd) {
    if (err) { throw 'could not open file: ' + err; }
    fs.write(fd, buffer, 0, buffer.length, null, function(err) {
        if (err) throw 'error writing file: ' + err;
        fs.close(fd, function() {
            // console.log('wrote the file successfully');
        });
    });
});

