## course-selector

[![Greenkeeper badge](https://badges.greenkeeper.io/cdaringe/course-selector.svg)](https://greenkeeper.io/)
Determine the optimal set of courses that a student should take provided relative _ratings_ on each course.  The objective is to maximize/minimize on the rating (e.g. maximize on course interest, or minimize on course difficulty).  Currently, the Georgia Tech [OMSCS courses](http://www.omscs.gatech.edu/courses/) are loaded into the repo, but can easily be swapped/forked/extended/yada-yada to accomodate any other course set or program set from another institution.

This code supports the optimiazation problem discussed @[cdaringe.com](http://cdaringe.com/applied-simplex-method-for-deciding-years-of-coursework/)

## usage
- See `course-list.js`.  Edit to fill with desired ratings.  Ensure all courses listed.  Note how duplicate numbered courses are formatted (special topics courses).
- See `tracks/xzy.js`.  Ensure that the tracks match current program requirements.
- Install nodejs+npm and python+pip.  After cloning the repo, `cd` to the directory and:
  - `npm install`
  - `pip install -r requirements.txt`
  - run `node index.js`
  - review output!

## disclaimer
Albeit that you can "minimize on difficulty" (_supposing you had "difficulty" data_), the capability to do so is a weak and subjective claim.  Attempting to do so will surely not work as intended.  School staff work dilligently to assert that each degree provides adequate challenges to its student body.  This is a tool intended to primarily to help students (myself), ensure that they pick the best courses aligned with their interests and learning goals.

## most importantly...
Don't forget to register on time and show up for class!  :pencil2::page_facing_up::eyeglasses::bell::school:
