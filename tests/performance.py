from datetime import datetime
import json
import sqlite3
from time import time

from opti_test import __version__
from opti_test.array_cable_problem import ArrayCableProblem


DB_NAME = "performance_opti_test.db"


def setup():
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS performance
             (Timestamp timestamp, Instance text, CodeVersion text, SolutionTime float, ObjectiveFunctionValue float)""")


def run_performance_test():
    setup()
    files = ["tests/test_cases/small.json", "tests/test_cases/medium.json", "tests/test_cases/large.json"]
    for input_file in files:
        with open(input_file, "r") as file:
            array_cable_problem = ArrayCableProblem(**json.load(file))
        start = time()
        array_cable_problem.create_layout()
        total_time = time() - start
        if array_cable_problem.layout is None:
            obj_value = 1e20
        obj_value = sum([c.get_cost() for c in array_cable_problem.layout.connections])
        with sqlite3.connect(DB_NAME) as connection:
            connection.execute(
                f"""INSERT INTO performance
                    VALUES
                        ('{datetime.now()}', '{input_file}', '{__version__}', {total_time}, {obj_value})
                """
            )


if __name__ == "__main__":
    run_performance_test()
