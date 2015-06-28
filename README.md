Entry reposted from [cdaringe.net](http://cdaringe.com/applied-simplex-method-for-deciding-years-of-coursework/)

I've been in college since 2005.  10 years.  It's earned me two BS's in engineering and a business minor.  Additionally, I've completed a Computer Science BS core cirriculum, omitting the traditional senior captstone, and am now heading straight for my CS masters.

Why am I getting a masters?  This is critical input to the model shortly discussed.  I am getting a masters for fun.  I am also getting it for simple self-improvement.  I have hope that the self-improvement acquired may enable me to acheive my goal of servitude, living in service for others, ideally while doing something I love.  It is not a decision rooted in career-advancement.  This fact sets the tone for the Model objective, `Z`, which we will visit momentarily.

The trouble with beginning my masters program is that there are many course options.  Within the program, there are various tracks (or specializations) that a student may take, and each student *must take one*.  Each track has its own subsets of categories comprised of courses.  Each category generally has credit hour requirements for those courses as well.

To clarify, suppose the program offers courses `c1, c2, ... , c100`.  `track1` may require that you take at least one course from (`c1, c3` ) and at least one course from (`c2, c10`).  `track2` may require 2 courses from (`c2, c3, c30`), and so on.  There may be 1 course per category, or there may be 100 courses per category.  At my current school of enrollement, I have observed as many as four of these categories falling underneath a single track.  I have even observed track catagories define rules that consume each other!

For instance, consider `track3`.  `track3` may represent a CS degree with a speciality in robotics.  Suppose `track3` has the following category set:

- `track3_category_1`: take one course from (`c1, c2, c3`)
- `track3_category_2`: take one course from (`c2, c4, c40`)
- `track3_category_3`: take at least 3 courses from `track3_category_1` & `track3_category_2`, i.e. category_3 is a composite category of category_1 & category_2.

Add more courses and more category conditions, and you can begin to see that even within a track, you can receive a very different education experience.

Well, why I am doing a masters, again?  For fun!  I want to take courses that I am most interested in.  I want to maximize [`fun` in school](https://www.youtube.com/watch?v=zzVB3zHeh4U).

Suppose I rank my courses, where courses just get less-desireable as the course number increases:

- c1 - I can't wait to take this course!
- c2 - I definitely want to take this course.
<br>...
- c30 - *grumble* the school mandates i take this
<br>...
- c100 - *no one wants to take this silly course!*

Suppose that program mandates that I take 10 courses, and that I am interested in only doing the minimum courses to graduate.  How do you begin picking which track to take?

One could brute force through a web of combinatorics and complicated coding to find the optimal solution.  The alternative, as I propose, is to format this problem of course **assignment** as an elegant [Mixed Integer Programming](https://en.wikipedia.org/wiki/Integer_programming) model.  Operations Researchers and Industrial Engineers (yours truly) are trained in this awesome art!  Here's what I do:

Set the objective function:
`(Maximze) Z = c1*C1_DESIRABLITY + c2*C1_DESIRABILITY ... cN*CN_DESIREABILITY`
<br>where
`Z` ~= integer representation of net-fun,
`cX` ~= boolean indicator if I take the course named `cX`
`CX` ~= numeric "desire" to take `cX`

Build a set of constraints to model:

- take just one track in the program
   - `track1 + track2 ... + trackN = 1`
- take the required number of graduation credits
    - `c1 + c2 ... + cN = 1`
- satisfy taking the # of courses required by *each* track category
    - `c1 + c2 + c3 - 2*track1 >= 0`, meaning at least 2 of c1, c2, or c3 must be taken if track 1 is selected
- take sufficient _foundational_ courses to sasify overall program requirements

I now must generate a course-wise ranking system to feed the model.  Rank all courses.  Certain factors are particulary difficult to model.  For instance, I omit scheduling, course availability, and professor influence when I generated my _personal_ desirability ranking.  These factors could all be modeled, but I leave them out for simplicity.  Accepting PRs :)  Note that there are some interesting things you can do with these factors.  Applying sufficiently large or low (negative, even) ranking points can force the algorithm to put you in a course, or help you dodge a course entirely if at all possible.  There are limits on its ability to do this, but know that it's a _feature_ of this model.

Enter these into the Simplex algorithm, and allow it to hunt for a potential solution!  After all was said and done, my model predicted that my interests fall most inline with the "Machine Learning" track, and assigned me the associated courses to satisfy that path!

https://github.com/cdaringe/course-selector

I tend to stick to javascript whenever feasible, however, Linear Programming packages in the JS community lack Integer & Binary variable support out-of-the box.  Thus, I have implemented my solution in Python using the rad++ [Pulp](http://www.coin-or.org/PuLP/) package.

<sup>Note: You dont _actually_ need to pick a track/specialization @my current school.  However, for the sake of an interesting problem, suppose that I, the student, strongly value having the speciality badge!</sup>

## usage
You must install nodejs/npm and python with pip.
- `npm install`
- `pip install -r requirements.txt`
- modify `coins-list.js` to specify your own rating values
- run `node index.js`
- review output!