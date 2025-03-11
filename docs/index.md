# Testing optimization code

## TL,DR;
- I differentiate between **unit** and **performance** tests: unit tests assess correctness, performance tests assess speed

### Unit testing
- Most of optimization code is like regular code, and it can be unit tested the same way.
- Unit testing a model is often difficult, as it is difficult to break it down into smaller parts (units). **Property-based testing** using very small instances often is a good tool here. Python has the `hypothesis` framework for this.
- One can spend time on unit testing individual equations, however I have found this to not add a lot of value.
- Modeling frameworks can be a way to get around license limitations for a commercial solver when testing (looking at you, Gurobi). However, I recommend that you run the full test suite with the real (i.e. production) configuration at least once before releasing.

### Performance testing
- For performance testing, we need three things: **real instances**, **real hardware**, **real setup**. If one of these is missing, the test does not mean much.
- If performance matters, then **performance testing is as important as unit testing**.
- The same patterns as in unit testing apply: **arrange**, **act**, **assert**. For performance tests, it can be useful to also record performance metrics over time, such as time, objective function value etc. A simple database can be a valuable friend.
- Performance testing gets easier when an API or CLI is available. Writing them is easy, and they save a lot of time.

## Learn more

Was the TL,DR; not enough? Then let's dive in :)
- [Introduction](./introduction.md): Why is testing powerful? Can it really work for optimization applications?
- [Principles of testing](./principles_of_testing.md): What is a unit, integration and performance test? What makes a test good? What is a property-based test?
- [Examples for unit testing](./unit-tests.md): How to think about unit tests for optimization code, based on a few example from the code in the repository.
- [Examples for performance testing](./performance-tests.md): A small performance testing setup for the code in the repository.

## Liked what you read?

Contribute! Leave a star on [Github](https://github.com/RichardOberdieck/opti_test)! Give me a shout on [bsky](https://bsky.app/profile/richardoberdieck.bsky.social) or [LinkedIn](https://www.linkedin.com/in/oberdieck/)! Check out my [website](https://oberdieck.dk).
