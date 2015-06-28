Entry reposted from [cdaringe.net](http://cdaringe.com/applied-simplex-method-for-deciding-years-of-coursework/)

## usage
The courses and specializations in this repo are from the [Georgia Tech OMSCS program](www.omscs.gatech.edu/).  Extending this to other schools should be no-biggie!
I represent all course and track metadata in javascipt primatives.  See `course-list.js` and `tracks/xzy.js`.
To run the program, you must install nodejs/npm and python with pip.  After cloning the repo, `cd` to the directory and:

- `npm install`
- `pip install -r requirements.txt`
- modify `course-list.js` to specify your own rating values
- run `node index.js`
- review output!

Don't forget to register on time and show up for class!  :pencil2::page_facing_up::eyeglasses::bell::school:

## post
I am pursuing a Masters of Computer Science.  Why?  Because learning is **fun**, I desire self-improvement, and because I can.  I hope that the gains acquired from the degree support [my goal of servitude](http://cdaringe.com/about/#workphilosophy) while doing something that I love.  This is not a pursuit rooted in career-advancement.  Understanding the motivation for the learning drives my proposed model's objective, generally dubbed `Z`, which describes the target value I want to maximize at @school.  Before we can break down what `Z` is and the components involved, allow me to set the context.

The trouble with beginning my masters program is that there are _many_ course options.  Within the program, there are various tracks (or specializations) that a student may take, and each student *must select a track*.  Each track has its own subsets of course categories, generally comprised of inter-related courses.  Each category generally has minimum credit hour requirements for the courses in the set.

To clarify, suppose the program offers courses `c1, c2, ... , c100`.  `track1` may require that you take at least one course from (`c1, c3` ) and at least one course from (`c2, c10`).  `track2` may require 2 courses from (`c2, c3, c30`), and so on.  There may be 1 course per category, or there may be 100 courses per category.  At my current school of enrollement, I have observed as many as four of these categories falling underneath a single track.  I have even observed track catagories define rules that consume each other!

Consider a hypothetical `track3`.  `track3` may represent a CS degree with a speciality in robotics.  Suppose `track3` has the following category set:

- `category_1`: take one course from (`c1, c2, c3`)
- `category_2`: take one course from (`c2, c4, c5`)
- `category_3`: take at least 3 courses from `category_1` & `category_2`. In this case, `category_3` is a composite category of `category_1` & `category_2`.

Add more courses and more category conditions, and you may begin to see that even within a track, you can receive a very different education experience.

I want to take courses that I am most interested in.  I want to maximize [`fun`](https://www.youtube.com/watch?v=zzVB3zHeh4U) in school.  The objective variable, `Z`, which I mentioned earlier, will represent fun in school.  Using a [Binary Integer Program](https://en.wikipedia.org/wiki/Integer_programming) (BIP), I suggest  a model to assert that I get the maximum fun out of my courses.  I achieve this by modeling real school-imposed constraints in a basic mathmatical form, as required by the BIP.  The BIP uses the over-arching program constraints, the  track & category constraints, and the amount of fun that each course is to find an optimal solution using the [simplex method](https://en.wikipedia.org/wiki/Simplex_algorithm).

Cool.  Let's try it.  Set the objective function:
`(Maximze) Z = c1*C1_DESIRABLITY + c2*C2_DESIRABILITY ... cN*CN_DESIREABILITY`
<br>where

- `Z` ~= integer representation of net-fun,
- `cX` ~= boolean indicator if I take the course named `cX`, and
- `CX` ~= numeric "desire" to take `cX`

Build a set of constraints to model:

- take just at least one track in the program
   - `track1 + track2 ... + trackN >= 1`
- take the required number of graduation credits
    - `c1 + c2 ... + cN = 30`
- satisfy taking the # of courses required by *each* track category
    - `c1 + c2 + c3 - 2*track1 >= 0`, meaning at least 2 of c1, c2, or c3 must be taken if track 1 is selected
- take sufficient _foundational_ courses to sasify overall program requirements
    - `c1 + c9 + c10 >= 2`, where c1, c9, and c10 are the foundational courses in the program

I now must generate a course-wise score system to feed the model.  Score all courses in 'fun'-ness.  Certain contributing factors are particulary difficult to model.  For instance, I omit scheduling, course availability, and professor influence when I generated my _personal_ desirability ranking.  These factors could all be modeled, but I leave them out for simplicity.  Accepting PRs :)  Note that there are some interesting things you can do with these factors.  Applying sufficiently large or low (negative, even) ranking points can force the algorithm to put you in a course, or help you dodge a course entirely if at all possible.  There are limits on its ability to do this, but know that it's a _feature_ of this model.

Enter these into the Simplex algorithm, and allow it to hunt for a potential solution!   The actual model is very small, and [can be viewed here](https://github.com/cdaringe/course-selector/blob/master/main.py).  After all was said and done, my model predicted that [my interests](https://github.com/cdaringe/course-selector/blob/master/ex/my-courses.js) fall most inline with the "Machine Learning" track, and assigned me the associated courses to satisfy that path!

```bash
('Status:', 'Optimal') // a maximized solution was found!
('track:_machine_learning', '=', 1.0) // 1 of 5 tracks was picked
('course:_Computational_Complexity_Theory_6520', '=', 1.0)
('course:_Data_and_Visual_Analytics_6242', '=', 1.0)
('course:_Distributed_Computing_7210', '=', 1.0)
('course:_Internetworking_Architectures_and_Protocols_7260', '=', 1.0)
('course:_Introduction_to_Operating_Systems_8803_002', '=', 1.0)
('course:_Machine_Learning_7641', '=', 1.0)
('course:_Pattern_Recognition_7616', '=', 1.0)
('course:_Software_Analysis_and_Testing_6340', '=', 1.0)
('course:_Software_Architecture_and_Design_6310', '=', 1.0)
('course:_Special_Topics:_Big_Data_for_Health_Informatics_8803_BDHI', '=', 1.0)
```

https://github.com/cdaringe/course-selector

I tend to stick to javascript whenever feasible, however, Linear Programming packages in the JS community lack Integer & Binary variable support out-of-the box.  Thus, I have implemented my solution in Python using the rad++ [Pulp](http://www.coin-or.org/PuLP/) package.

<sup>Note: You dont _actually_ need to pick a track/specialization @my current school.  However, for the sake of an interesting problem, suppose that I, the student, strongly value having the speciality badge!</sup>
