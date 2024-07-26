import pandas as pd
import plotly.graph_objs as go
import plotly.colors
from plotly.subplots import make_subplots


def load_data(file_path):
    # Load the data, skipping the first 7 rows
    df_data = pd.read_excel(file_path, sheet_name='Foundation Reactions', skiprows=7, header=None)
    df_data.columns = ['Support', "X Coordinate", "Y Coordinate", "Z Coordinate", "TBR", "TBR", "TBR", "Combination", "Fx [kN]", "Fy [kN]", "Fz [kN]", "Mx [kNm]", "My [kNm]", "Mz [kNm]"]
    df_data.drop(df_data.columns[[4, 5, 6]], axis=1, inplace=True)
    
    # Find the row with "Wall Supports"
    wall_supports_index = df_data[df_data['Support'] == 'Wall Supports'].index[0]
    
    # Remove two rows before and all rows after "Wall Supports"
    df_data = df_data.iloc[:wall_supports_index - 2]

    df_data_first_part = df_data.iloc[:, :4]
    df_data_rest = df_data.iloc[:, 4:]
    df_data_first_part = df_data_first_part.ffill(axis=0)
    df_data = pd.concat([df_data_first_part, df_data_rest], axis=1)

    df_data.set_index(['Support', df_data.groupby('Support').cumcount() + 1], inplace=True)
    df_data.index.names = ['Support', '']

    return df_data

def find_extremes(series, combinations):
    if series.isnull().all():
        return 0, "-", 0, "-"

    max_positive = series[series > 0].max()
    max_negative = series[series < 0].min()

    max_positive_combination = "-" if pd.isnull(max_positive) else combinations[series.idxmax()]
    max_negative_combination = "-" if pd.isnull(max_negative) else combinations[series.idxmin()]

    max_positive = 0 if pd.isnull(max_positive) else max_positive
    max_negative = 0 if pd.isnull(max_negative) else max_negative

    return max_positive, max_positive_combination, max_negative, max_negative_combination

def generate_data_for_display(df_data):
    # I took a try at removing all of the accumulators and manual DataFrame building
    # See below. Your 'find_extremes' function is what makes all of this work!

    df_acc = pd.DataFrame()
    for force_col in ['Fx [kN]', 'Fy [kN]', 'Fz [kN]', 'Mx [kNm]', 'My [kNm]','Mz [kNm]']:
        force_dir = force_col.split(" ")[0]

        # The next line creates a series with an index of "Support" but each cell contains a tuple of the four values
        # So we need to split the values out of tuples and into their own separate columns
        # This find_extremes function is great (well done!) Let's use it in .apply!
        result_series = df_data.groupby(['Support']).apply(lambda x: find_extremes(x[force_col], x['Combination']))
        enveloped_column_names = (
            f"Max +{force_dir}", 
            f"Max +{force_dir} Combination", 
            f"Max -{force_dir}", 
            f"Max -{force_dir} Combination"
        )

        # If the result is a series of tuples (with an index), then if we convert the series to a list then we have
        # a list of tuples which can be used to create a new df with however-many-rows x four-columns
        enveloped_df = pd.DataFrame(data = result_series.to_list(), index=result_series.index, columns=enveloped_column_names)
        df_acc = pd.concat([df_acc, enveloped_df], axis=1)
    
    # Last, we need to add the X, Y, Z coordinates. 
    # If our indexes match, then we can just add the columns onto our 'df_acc'
    # without needing to do anything fancy.

    coords_df = df_data.reset_index().loc[:, ['Support', 'X Coordinate', 'Y Coordinate', 'Z Coordinate']].drop_duplicates()
    coords_df = coords_df.set_index(['Support'])
    
    new_df = pd.concat([coords_df, df_acc], axis=1).reset_index() # Take "Support" out of the index and back in to the columns

    return new_df

def calculate_piles(safe_capacity, max_load):
    if safe_capacity <= 0:
        return 0
    return -(-max_load // safe_capacity)  # Ceiling division

def generate_plot(option, new_df, safe_pile_capacity=None, safe_pile_tensile_capacity=None):
    fig = go.Figure()

    if safe_pile_capacity is not None:
        safe_pile_capacity = float(safe_pile_capacity)
        if not (100 < safe_pile_capacity <= 10000):
            raise ValueError("Pile capacity is too low or too high")

    if safe_pile_tensile_capacity is not None:
        try:
            safe_pile_tensile_capacity = float(safe_pile_tensile_capacity)
            if safe_pile_tensile_capacity >= 0:
                raise ValueError("Please enter a negative value for tensile capacity")
        except ValueError:
            raise ValueError("Invalid input for tensile capacity")
    else:
        safe_pile_tensile_capacity = None

    if option == 'Coordinates':
        unique_z_levels = new_df['Z Coordinate'].unique()
        fig = go.Figure()

        for z in unique_z_levels:
            df_z = new_df[new_df['Z Coordinate'] == z]
            trace = go.Scatter(
                x=df_z['X Coordinate'],
                y=df_z['Y Coordinate'],
                mode='markers+text',
                marker=dict(size=10),
                text=df_z['Support'],
                name=f'Z = {z}'
            )
            fig.add_trace(trace)

        fig.update_layout(
            title='Support Coordinates',
            xaxis_title='X Coordinate',
            yaxis_title='Y Coordinate',
        )

    elif option == 'Number of Piles':
        if safe_pile_capacity is None:
            raise ValueError("Safe pile capacity must be provided for 'Number of Piles' option")

        # Calculate required piles
        max_loads = new_df[['Max +Fz', 'Max -Fz']].max(axis=1)  # Taking maximum values
        max_loads[max_loads < 0] = 0  # Setting negative values to 0
        required_piles = max_loads.apply(lambda x: calculate_piles(safe_pile_capacity, x))

        # Define color mapping based on number of piles
        color_map = {
            1: 'blue',
            2: 'red',
            3: 'green',
            4: "black",
            5: "orange",
            6: "brown",
            7: "yellow",
            8: "pink"
    
        }

        traces = []
        for pile_number, color in color_map.items():
            df_pile = new_df[required_piles == pile_number]
            trace = go.Scatter(
                x=df_pile['X Coordinate'],
                y=df_pile['Y Coordinate'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=color,
                    line=dict(width=1, color='DarkSlateGrey')
                ),
                name=f'{pile_number} Piles'
            )
            traces.append(trace)

        for trace in traces:
            fig.add_trace(trace)

        fig.update_layout(
            title='Number of Piles required for each Support',
            xaxis_title='X Coordinate',
            yaxis_title='Y Coordinate',
            hovermode='closest'
        )

    # I also removed the repetitive plotting code. They all seemed to be exactly the same
    # except for the hover labels so I parametrized the hover labels so you only need one
    elif 'maximum' in option.lower():
        force_dir = option.split()[-1]
        max_primary = new_df[f'Max +{force_dir}']
        max_secondary = new_df[f'Max -{force_dir}']

        fig = make_subplots(rows=2, cols=1)

        hovertext01 = new_df.apply(
            lambda row: (
                f'Support: {row["Support"]}<br>'
                f'Max +{force_dir}: {row[f"Max +{force_dir}"]} kN<br>'
                f'Combination +Fx: {row[f"Max +{force_dir} Combination"]}'
            ), axis=1
        )
        hovertext02 = new_df.apply(
            lambda row: (
                f'Support: {row["Support"]}<br>'
                f'Max -{force_dir}: {row[f"Max -{force_dir}"]} kN<br>'
                f'Combination -Fx: {row[f"Max -{force_dir} Combination"]}'
            ), axis=1
        )

        fig.add_trace(go.Bar(
            x=new_df['Support'],
            y=max_primary,
            name=f'Maximum +{force_dir}',
            text=hovertext01,
            hoverinfo='text'
        ), row= 1, col= 1)
        fig.add_trace(go.Bar(
            x=new_df['Support'],
            y=max_secondary,
            name=f'Maximum -{force_dir}',
            text=hovertext02,
            hoverinfo='text'
        ), row=1, col=1)

        scatter_color = 'blue' # Adjust scatter color based on option
        hovertext03 = new_df.apply(
            lambda row: (
                f'Support: {row["Support"]}<br>'
                f'Max +{force_dir}: {row[f"Max +{force_dir}"]} kN<br>'
                f'Max -{force_dir}: {row[f"Max -{force_dir}"]} kN<br>'
                f'Combination +{force_dir}: {row[f"Max +{force_dir} Combination"]}<br>'
                f'Combination -{force_dir}: {row[f"Max -{force_dir} Combination"]}'
            )
            ,axis=1
        )

        fig.add_trace(go.Scatter(
            x=new_df['X Coordinate'],
            y=new_df["Y Coordinate"],
            mode='markers',
            marker=dict(color=scatter_color),
            name=f"Max [+/-] {force_dir}",
            text=hovertext03,
            hoverinfo='text'
        ), row=2, col=1)

        fig.update_layout(
        title=f'Maximum {force_dir} and Support Coordinates',
        autosize=False,
        width=1300,
        height=900 
        
        )

        fig.update_yaxes(automargin=True)
    
    else:
        raise ValueError(f"Invalid option {option}.")


    return fig