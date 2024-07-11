import streamlit as st
from functions import load_data, generate_data_for_display, generate_plot
import os

def main():
    st.title('Foundation Reactions Analysis')

    # Option to upload file or use example file
    st.sidebar.header('Upload your Excel file')
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=['xls', 'xlsx'])

    use_example = st.sidebar.checkbox('Use example Excel file')
    example_file_path = 'TSD Foundation Reaction Export.xlsx'  # Default example file path

    if use_example:
        if os.path.exists(example_file_path):
            file_path = example_file_path
        else:
            st.sidebar.error('Example file not found. Please upload your own Excel file.')
            return
    elif uploaded_file:
        file_path = uploaded_file
    else:
        st.sidebar.warning('Please upload an Excel file or choose to use the example file.')
        return

    # Load the data
    df_data = load_data(file_path)

    # Generate the data for display
    new_df = generate_data_for_display(df_data)

    # Plot initial coordinates
    st.subheader("Support Points Coordinates")
    st.plotly_chart(generate_plot("Coordinates", new_df))

    # Dropdown menu for selecting the maximum forces and moments
    option = st.selectbox('Choose an option:', ['Maximum Fx', 'Maximum Fy', 'Maximum Fz', 'Maximum Mx', 'Maximum My', 'Maximum Mz'])

    # Inputs for safe pile capacity and tensile capacity
    safe_pile_capacity = st.number_input('Safe Pile Capacity [kN]:', min_value=100.0, max_value=10000.0, step=1.0, value=600.0)
    safe_pile_tensile_capacity = st.number_input('Safe Pile Tensile Capacity [kN] (optional, enter negative value):', value=-100.0)
    st.write("(Note: Please enter a negative value for tensile capacity)")

    # Button to generate the plot
    if st.button('Generate Now'):
        st.plotly_chart(generate_plot(option, new_df, safe_pile_capacity, safe_pile_tensile_capacity))

if __name__ == '__main__':
    main()

