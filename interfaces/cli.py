import json
import click

from opti_test.classes import ArrayCableProblem


@click.command
@click.option("--input_file", help="json file with the input data")
@click.option("--output_file", default="results.json", help="json file with the results")
def run(input_file: str, output_file: str):
    array_cable_problem = ArrayCableProblem.validate_json(json.loads(input_file))
    array_cable_problem.create_layout()
    if array_cable_problem.layout is not None:
        with open(output_file, "w") as file:
            file.write(array_cable_problem.layout.model_dump_json())


if __name__ == "__main__":
    run()
