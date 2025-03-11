import json
from opti_test.array_cable_problem import ArrayCableProblem
import streamlit as st


def main():
    st.title("Array cable optimization")
    st.sidebar.header("Navigation")
    option = st.sidebar.radio(" ", ("Application", "Documentation"))

    if option == "Application":
        uploaded_file = st.file_uploader("Get input file (.json)", type="json")
        if uploaded_file is not None:
            data = json.load(uploaded_file)
            array_cable_problem = ArrayCableProblem(**data)
            st.write(array_cable_problem.plot(False))
            is_optimize = st.button("Optimize")
            if is_optimize:
                array_cable_problem.create_layout()
                st.header("Layout")
                st.write(array_cable_problem.plot(False))

    if option == "Documentation":
        with open("docs/index.md", "r") as file:
            st.write(file.read())


if __name__ == "__main__":
    main()
