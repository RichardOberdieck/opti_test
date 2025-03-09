import streamlit as st
from opti_test.layout_data import read_excel


def main():
    st.title("Array cable optimization")
    st.sidebar.header("Navigation")
    option = st.sidebar.radio(" ", ("Application", "Documentation"))

    if option == "Application":
        uploaded_file = st.file_uploader("Get input file (.xlsx)", type="xlsx", encoding=None)
        if uploaded_file is not None:
            cable_problem = read_excel(uploaded_file)
            st.write(cable_problem.plot(False))
            is_optimize = st.button("Optimize")
            if is_optimize:
                cable_problem.solve()
                st.header("Layout")
                st.write(cable_problem.plot(False))

    if option == "Documentation":
        fo = open("doc/notes.md", "r")
        st.write(fo.read())


if __name__ == "__main__":
    main()
