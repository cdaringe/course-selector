'use strict';
var pyshell = require('python-shell');
var _ = require('lodash');

// load in masters program track options
var courses = require('./course-list.js');
var courseNums = _.pluck(courses, 'num');
var courseNames = _.pluck(courses, 'name');
var track1 = require('./track/perception-robotics.js');
var track2 = require('./track/programming-systems.js');
var track3 = require('./track/high-performance-computing.js');
var track4 = require('./track/machine-learning.js');
var track5 = require('./track/interactive-intelligence.js');
var tracks = [track1, track2, track3, track4, track5];
var courseMismatch = [];
var _tracks = {};

var coursesByNum, coursesByNumKeys;
var ratingsByNum, ratingsByNumKeys;
var ratingMismatch;
var currTrack;


// populate all tracks
for (var i = tracks.length - 1; i >= 0; i--) {
    currTrack = tracks[i];
    _tracks[currTrack.name] = { catagories: currTrack.catagories }; // addtl meta loaded in in py process
}

coursesByNum = _.indexBy(courses, 'num');

// > no course # duplicated (course number is our unique key)
if (courseNums.length !== _.unique(courseNums).length) {
    var results = [], sorted = _.sortBy(courseNums);
    for (var i = 0; i < courseNums.length - 1; i++) {
        if (sorted[i + 1] == sorted[i]) {
            results.push(sorted[i]);
        }
    }
    throw new Error('duplicate courses numbers found: ' + results.join(', '));
}

// > no unhandled course description duplicates
if (courseNames.length !== _.unique(courseNames).length) {
    results = [];
    sorted = _.sortBy(courseNames);
    for (i = 0; i < courseNames.length - 1; i++) {
        if (sorted[i + 1] == sorted[i]) {
            results.push(sorted[i]);
        }
    }
    throw new Error('duplicate courses names found: ' + results.join(', '));
}

tracks.forEach(function assertTrackCoursesValid(track) {
    track.catagories.forEach(function assertCategoryCoursesValid(catagory) {
        catagory.courseNums.forEach(function assertCourseValid(courseNum) {
            if (!coursesByNum[courseNum]) {
                courseMismatch.push(track.name + ' ' + courseNum);
            }
        });
    });
});

if (courseMismatch.length) {
    console.dir(courseMismatch);
    throw new Error('track courses are not in master course list. see above');
}

// problem definition in json set to match expected format in
// python LP processing script.  see main.py
var problem = {
    collegeCredits: 30,
    foundationalCourses: 2,
    courses: coursesByNum,
    tracks: _tracks,
    rating: ratingsByNum
};

var options = {
    mode: 'text',
    args: [JSON.stringify(problem)],
    scriptPath: './'
};

pyshell.run('./main.py', options, function (err, results) {
    if (err) {
        throw err;
    }
    console.log(results.join("\n"));
});
