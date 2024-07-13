import streamlit as st
from functions import load_data, generate_data_for_display, generate_plot
import os



def main():
    st.title('TSD Support Reactions')

    # Option to upload file or use example file
    st.sidebar.header('Upload your Excel file')
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=['xls', 'xlsx'])

    use_example = st.sidebar.checkbox('Use example Excel file')
    example_file_path = 'TSD Steel Frame Example.xlsx'  # Default example file path

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

    with st.sidebar.expander("Instructions"):
        st.write("""
        - In the Tekla Structural Designer menu bar go to Report and select "Foundation Reaction". \n
        - Make sure that "All combinations" option is selected in "Loading Filter" \n
        - Make sure that "Service" is selected in "Combination Factors" in the report structure settings. 
                 
        (Note: Wall supports are beyond scope)
        """)

    # Load the data
    df_data = load_data(file_path)

    # Generate the data for display
    new_df = generate_data_for_display(df_data)

    # Plot initial coordinates
   
    st.plotly_chart(generate_plot("Coordinates", new_df))

    # Dropdown menu for selecting the maximum forces and moments
    option = st.selectbox('Choose an option:', ["Number of Piles", 'Maximum Fx', 'Maximum Fy', 'Maximum Fz', 'Maximum Mx', 'Maximum My', 'Maximum Mz'])

    # Inputs for safe pile capacity and tensile capacity
    safe_pile_capacity = st.number_input('Safe Pile Axial Capacity [kN]:', min_value=100.0, max_value=10000.0, step=1.0, value=600.0)
    safe_pile_tensile_capacity = st.number_input('Safe Pile Tensile Capacity [kN] (optional, enter negative value):', value=-100.0)
    st.write("(Note: Wall supports are beyond scope)")

    # Button to generate the plot
    if st.button('Generate Now'):
        st.plotly_chart(generate_plot(option, new_df, safe_pile_capacity, safe_pile_tensile_capacity))

if __name__ == '__main__':
    main()



