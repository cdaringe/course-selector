#!/usr/bin/env python
import argparse
import sys
import json
from pulp import *

parser = argparse.ArgumentParser(description='Solve the course selection linear program')
parser.add_argument('problem', metavar='p', type=str, nargs='+',
                   help='yaml string defining the mathematical LP')

# solve the ideal course and program layout
def main(data):
    prob = LpProblem("The Course Selection Problem", LpMaximize)

    foundationalCourses = data['foundationalCourses']
    collegeCredits = data['collegeCredits']
    courses = data['courses']
    tracks = data['tracks']

    foundational = []
    online = []

    # course switches
    for id in courses:
        course = courses[id]
        course['_LpVariable'] = LpVariable(name = 'course: ' + course['name'] + ' ' + course['num'], lowBound = 0, upBound = 1, cat = LpInteger)
        if course['foundational']:
            foundational.append((course['_LpVariable'], 1))
        if course['online']:
            online.append((course['_LpVariable'], course['credits']))

    # track switches
    for trackName, track in tracks.iteritems():
        track['_LpVariable'] = LpVariable(name = 'track: ' + trackName, lowBound = 0, upBound = 1, cat = LpInteger)

    # z - maximize rating
    prob += LpAffineExpression(
        [ (course['_LpVariable'], course['rating']) for courseNum, course in courses.iteritems() ] # c1*d1 + c2*d2 ...
    )

    # ensure that minimum# foundational courses are taken
    prob += LpConstraint(LpAffineExpression(foundational), LpConstraintGE, str(foundationalCourses) + ' foundational courses selected', foundationalCourses)

    # OPTIONAL - comment on/off as desired
    # ensure that only courses are online (i.e. that online credits >= required credits)
    prob += LpConstraint(LpAffineExpression(online), LpConstraintGE, str(collegeCredits) + ' online credits selected', collegeCredits)

    # constrain total # of credit hours in program to college requirement
    constraintTotalCredits = LpAffineExpression(
        [ (course['_LpVariable'], course['credits']) for courseNum, course in courses.iteritems() ]
    )
    prob += LpConstraint(constraintTotalCredits, LpConstraintEQ,  "total credits = college requirement", collegeCredits)

    # contrain student to a single track
    constraintSingleTrack = LpAffineExpression(
        [ (tracks[trackName]['_LpVariable'], 1) for trackName, track in tracks.iteritems() ]
    )
    prob += LpConstraint(constraintSingleTrack, LpConstraintGE,  "single track selected", 1)

    # constrain track to track groupings
    for trackName, track in tracks.iteritems():
        groupNdx = 0
        for group in track['catagories']:
            minCoursesGroupReqOffset = (tracks[trackName]["_LpVariable"], -1 * group["required"])
            minCoursesGroupReq = [ (courses[id]['_LpVariable'], 1) for id in group["courseNums"] ]
            minCoursesGroupReq.insert(0, minCoursesGroupReqOffset)
            prob += LpConstraint(
                LpAffineExpression(minCoursesGroupReq),
                LpConstraintGE,
                "must take " + str(group["required"]) + " courses in grouping" + str(groupNdx) + " in track " + str(trackName),
                0
            )
            groupNdx += 1

    # TODO constrain 4000/5000 level courses (that are the same course, from getting double credit)

    prob.writeLP("courses.lp")
    prob.solve()
    print("Status:", LpStatus[prob.status])
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    return 0

def entry_point():
    args = parser.parse_args()
    problem = json.loads(args.problem[0])
    raise SystemExit(main(problem))
        # 'collegeCredits': 6,
        # 'courses': {
        #     0: {'name': "course1", 'credits': 3, 'rating': 1 }, # courseId: meta
        #     1: {'name': "course2", 'credits': 3, 'rating': 1 },
        #     2: {'name': "course3", 'credits': 3, 'rating': 1}
        # },
        # 'tracks': {
        #     'track1': {
        #         '_LpVariable': None,
        #         'catagories': [ # list course groupings
        #             {
        #                 'name': 'track1_category1',
        #                 'courseNums': [0],
        #                 'required': 1
        #             },
        #             {
        #                 'name': 'track1_category2',
        #                 'courseNums': [1],
        #                 'required': 1
        #             }
        #         ]
        #     },
        #     'track2': {
        #         '_LpVariable': None,
        #         'catagories': [
        #             {
        #                 'name': 'track2_category1',
        #                 'courseNums': [1, 2],
        #                 'required': 2
        #             }
        #         ]
        #     },
        #     'track3': {
        #         '_LpVariable': None,
        #         'catagories': [
        #             {
        #                 'name': 'track3_category1',
        #                 'courseNums': [0, 2],
        #                 'required': 2
        #             }
        #         ]
        #     }
        # }


if __name__ == '__main__':
    entry_point()
