var data = require('./student-performance-data');
var _ = require('lodash');
var dataByCourseNumber = _.groupBy(data, 'course');
var fs = require('fs');
var result = [];

_.forOwn(dataByCourseNumber, function(semesterSet, courseNum) {
    var perfPoints = semesterSet.filter(function(semester) { return !!semester.percentHighScore; }); // filter out 0's
    if (!perfPoints.length) return;
    result.push({
        course: courseNum,
        percentHighScore: perfPoints.reduce(function(prev, semester) { return prev + semester.percentHighScore; }, 0) / perfPoints.length
    });
});

fs.writeFileSync('./result', JSON.stringify(result,null,2));