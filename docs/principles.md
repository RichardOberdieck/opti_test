# Principles of testing

## The basics

A test should always test "one thing". In other words, in an ideal world, there is a single question a test answers. Does this function return 4 when I provide 2 as an argument? Is the problem solved to optimality with an objective function value of 19.993? A new question, a new test.

The pattern to arrive at such structure is the **arrange**, **act**, **assert** structure. Let me show a small example:

```
def multiply(x, y):
    return x*y


def test_multiply():
    # Arrange
    x = 2
    y = 5

    # Act
    result = multiply(x, y)

    # Assert
    assert 10 == result
```

The comments are critical by the way. Believe it or not, **I actually add them to every test I write, always**. Ask my colleagues. They think it is slightly crazy. That's ok. To me, if I cannot segment my test into these three buckets, something is off. It shows what I am focussing on. It makes it very easy to understand.

## What type of testing is there?

There is no natural law for testing, just some people having opinions. Here are mine:
- A **unit test** is a test which covers a single function or method in a code base. Very rarely it may cover two, but that is the exception. As a rule of thumb, every function or method should be tested.
- An **integration test** is a test which covers a certain "part" of the code, or an expected flow of data through the application. It is by definition more high-level than a unit test, and combines different components to check whether that part of the application is behaving as expected. Sometimes, we also call something an integration test if it uses actual database access or takes a long time to run.
- An **end-to-end test** runs the entire application end to end (as the name suggests). It is the most high-level type of test.
- A **performance test** focusses on the performance of the application, typically something like throughput or accuracy.

> The lines between all of these are blurry.

## Property-based testing

Just watch [this](https://youtu.be/mkgd9iOiICc?si=9PsEzVk6ka4KmhFA).

Ok, if you are still reading: property-based testing means that instead of testing a specific case, we test a specific property. An example:

> When I run my function `multiply_by_2(x)`, is the result divisible by 2?

This works well for optimization models:

> Does the solution always connect all turbines?
> Do I get `None` if the problem is infeasible?
> Do I ever exceed the max number of cable types?

In other words: **does the solution follow what the equations should encode?**

So if it is so awesome, why don't we use property-based testing all the time? Two reasons:
1. The setup is laborious. ChatGPT can help here, but it still is not something I want to do for everything.
2. Because it tries to find a falsifying example, it runs through a lot of different combinations, which takes time. So if you have thousands of tests, this will become an issue.

Got it? Let's look at some [examples for unit testing](./unit-tests.md)!
