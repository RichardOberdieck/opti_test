---
marp: true
---

# Welcome

---

# Structure

1. Why is this a topic?
2. What is hard about testing optimization code?
3. Unit testing optimization code
4. Performance testing optimization code
5. Cake

---

# Why is this a topic?

Testing helps find problems before they become actual problems

<img src="https://motoroctane.com/wp-content/uploads/2020/11/car-testing.jpg?x46283" alt="car_testing" width="560"/>

<sub>https://motoroctane.com/wp-content/uploads/2020/11/car-testing.jpg?x46283</sub>


---

# What is hard about testing optimization code?

1. Most people who write optimization code have little experience writing unit tests
2. It often makes little logical sense to test sub-components of a mathematical model.

<img src="https://sharpmagazine.com/wp-content/uploads/2015/11/1100-1348x900.jpg" alt="watch" width="500"/>

---

# The test case today (insert pun-related laughter)

- How to connect wind turbines ("WTGs") to offshore substations ("OSS")

<img src="https://pub.mdpi-res.com/energies/energies-14-03615/article_deploy/html/images/energies-14-03615-g003.png?1624412096" alt="array_cable_problem" width="560"/>

<sub>https://pub.mdpi-res.com/energies/energies-14-03615/article_deploy/html/images/energies-14-03615-g003.png?1624412096</sub>

---

# Describing the model

- Minimize cost of cables
- Subject to
    - All turbines need to be connected
    - Flow balance (flow in + turbine power = flow out)
    - Respect flow limits on cable type
    - Cables cannot cross
    - Max number of different cable types

The detailed mathematical model can be found in the docs, or read Martina Fischetti's thesis.

---

# Let's have a look!

---

# Unit testing optimization code

- Unit = small component with expected behavior
- **Property-based testing** good approach for optimization models.
- Unit testing individual equations is too much
- Modeling frameworks can be a way to get around license limitations for a commercial solver when testing (looking at you, Gurobi).
- However, I recommend that you run the full test suite with the real (i.e. production) configuration at least once before releasing.

---

# Property-based testing

Instead of testing a specific case, we test a specific property. An example:

> When I run my function `multiply_by_2(x)`, is the result divisible by 2?

This works well for optimization models:

> Does the solution always connect all turbines?
> Do I get `None` if the problem is infeasible?
> Do I ever exceed the max number of cable types?

In other words: **does the solution follow what the equations should encode?**

Caveat: This **only** works with small instances in a somewhat reasonable time


---

# Performance testing optimization code

- **real instances**, **real hardware**, **real setup**
- Performance testing is as important as unit testing
- The same patterns as in unit testing apply: **arrange**, **act**, **assert**.
- Record performance metrics over time
- Create an API or CLI, they save a lot of time.

---

# Cake
