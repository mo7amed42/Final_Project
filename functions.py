import pandas as pd
import plotly.graph_objs as go
import plotly.colors

def load_data(file_path):
    df_data = pd.read_excel(file_path, sheet_name='Foundation Reactions', skiprows=7, header=None)
    df_data.columns = ['Support', "X Coordinate", "Y Coordinate", "Z Coordinate", "TBR", "TBR", "TBR", "Combination", "Fx [kN]", "Fy [kN]", "Fz [kN]", "Mx [kNm]", "My [kNm]", "Mz [kNm]"]
    df_data.drop(df_data.columns[[4, 5, 6]], axis=1, inplace=True)
    df_data = df_data.iloc[:-7]

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
    supports = []
    x_coordinates = []
    y_coordinates = []
    z_coordinates = []
    max_pos_fx = []
    max_pos_fx_comb = []
    max_neg_fx = []
    max_neg_fx_comb = []
    max_pos_fy = []
    max_pos_fy_comb = []
    max_neg_fy = []
    max_neg_fy_comb = []
    max_pos_fz = []
    max_pos_fz_comb = []
    max_neg_fz = []
    max_neg_fz_comb = []
    max_pos_Mx = []
    max_pos_Mx_comb = []
    max_neg_Mx = []
    max_neg_Mx_comb = []
    max_pos_My = []
    max_pos_My_comb = []
    max_neg_My = []
    max_neg_My_comb = []
    max_pos_Mz = []
    max_pos_Mz_comb = []
    max_neg_Mz = []
    max_neg_Mz_comb = []

    unique_supports = df_data.index.get_level_values('Support').unique()

    for support in unique_supports:
        x_coord = df_data.loc[support, 'X Coordinate'].unique()[0]
        y_coord = df_data.loc[support, 'Y Coordinate'].unique()[0]
        z_coord = df_data.loc[support, 'Z Coordinate'].unique()[0]

        max_positive_fx, max_positive_comb_fx, max_negative_fx, max_negative_comb_fx = find_extremes(df_data.loc[support]['Fx [kN]'], df_data.loc[support]['Combination'])
        max_positive_fy, max_positive_comb_fy, max_negative_fy, max_negative_comb_fy = find_extremes(df_data.loc[support]['Fy [kN]'], df_data.loc[support]['Combination'])
        max_positive_fz, max_positive_comb_fz, max_negative_fz, max_negative_comb_fz = find_extremes(df_data.loc[support]['Fz [kN]'], df_data.loc[support]['Combination'])
        max_positive_Mx, max_positive_comb_Mx, max_negative_Mx, max_negative_comb_Mx = find_extremes(df_data.loc[support]['Mx [kNm]'], df_data.loc[support]['Combination'])
        max_positive_My, max_positive_comb_My, max_negative_My, max_negative_comb_My = find_extremes(df_data.loc[support]['My [kNm]'], df_data.loc[support]['Combination'])
        max_positive_Mz, max_positive_comb_Mz, max_negative_Mz, max_negative_comb_Mz = find_extremes(df_data.loc[support]['Mz [kNm]'], df_data.loc[support]['Combination'])

        supports.append(support)
        x_coordinates.append(x_coord)
        y_coordinates.append(y_coord)
        z_coordinates.append(z_coord)
        max_pos_fx.append(max_positive_fx)
        max_pos_fx_comb.append(max_positive_comb_fx)
        max_neg_fx.append(max_negative_fx)
        max_neg_fx_comb.append(max_negative_comb_fx)
        max_pos_fy.append(max_positive_fy)
        max_pos_fy_comb.append(max_positive_comb_fy)
        max_neg_fy.append(max_negative_fy)
        max_neg_fy_comb.append(max_negative_comb_fy)
        max_pos_fz.append(max_positive_fz)
        max_pos_fz_comb.append(max_positive_comb_fz)
        max_neg_fz.append(max_negative_fz)
        max_neg_fz_comb.append(max_negative_comb_fz)
        max_pos_Mx.append(max_positive_Mx)
        max_pos_Mx_comb.append(max_positive_comb_Mx)
        max_neg_Mx.append(max_negative_Mx)
        max_neg_Mx_comb.append(max_negative_comb_Mx)
        max_pos_My.append(max_positive_My)
        max_pos_My_comb.append(max_positive_comb_My)
        max_neg_My.append(max_negative_My)
        max_neg_My_comb.append(max_negative_comb_My)
        max_pos_Mz.append(max_positive_Mz)
        max_pos_Mz_comb.append(max_positive_comb_Mz)
        max_neg_Mz.append(max_negative_Mz)
        max_neg_Mz_comb.append(max_negative_comb_Mz)

    new_data = {
        'Support': supports,
        'X Coordinate': x_coordinates,
        'Y Coordinate': y_coordinates,
        'Z Coordinate': z_coordinates,
        'Max +Fx': max_pos_fx,
        'Max +Fx Combination': max_pos_fx_comb,
        'Max -Fx': max_neg_fx,
        'Max -Fx Combination': max_neg_fx_comb,
        'Max +Fy': max_pos_fy,
        'Max +Fy Combination': max_pos_fy_comb,
        'Max -Fy': max_neg_fy,
        'Max -Fy Combination': max_neg_fy_comb,
        'Max +Fz': max_pos_fz,
        'Max +Fz Combination': max_pos_fz_comb,
        'Max -Fz': max_neg_fz,
        'Max -Fz Combination': max_neg_fz_comb,
        'Max +Mx': max_pos_Mx,
        'Max +Mx Combination': max_pos_Mx_comb,
        'Max -Mx': max_neg_Mx,
        'Max -Mx Combination': max_neg_Mx_comb,
        'Max +My': max_pos_My,
        'Max +My Combination': max_pos_My_comb,
        'Max -My': max_neg_My,
        'Max -My Combination': max_neg_My_comb,
        'Max +Mz': max_pos_Mz,
        'Max +Mz Combination': max_pos_Mz_comb,
        'Max -Mz': max_neg_Mz,
        'Max -Mz Combination': max_neg_Mz_comb,
    }

    new_df = pd.DataFrame(new_data)
    return new_df

def calculate_piles(safe_capacity, max_load):
    if safe_capacity <= 0:
        return 0
    return -(-max_load // safe_capacity)  # Ceiling division

def generate_plot(option, new_df, safe_pile_capacity=None, safe_pile_tensile_capacity=None):
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
            yaxis_title='Y Coordinate'
        )

        return fig

    elif option == 'Maximum Fx':
        max_Fx = new_df[['Max +Fx', 'Max -Fx']].max(axis=1)
        fig = go.Figure(data=[go.Bar(x=new_df['Support'], y=max_Fx, name='Maximum Fx')])
        fig.update_layout(
            title='Maximum Fx for each Support',
            xaxis_title='Support',
            yaxis_title='Maximum Fx (kN)'
        )
        return fig

    elif option == 'Maximum Fy':
        max_Fy = new_df[['Max +Fy', 'Max -Fy']].max(axis=1)
        fig = go.Figure(data=[go.Bar(x=new_df['Support'], y=max_Fy, name='Maximum Fy')])
        fig.update_layout(
            title='Maximum Fy for each Support',
            xaxis_title='Support',
            yaxis_title='Maximum Fy (kN)'
        )
        return fig

    elif option == 'Maximum Fz':
        max_Fz = new_df[['Max +Fz', 'Max -Fz']].max(axis=1)
        fig = go.Figure(data=[go.Bar(x=new_df['Support'], y=max_Fz, name='Maximum Fz')])
        fig.update_layout(
            title='Maximum Fz for each Support',
            xaxis_title='Support',
            yaxis_title='Maximum Fz (kN)'
        )
        return fig

    elif option == 'Maximum Mx':
        max_Mx = new_df[['Max +Mx', 'Max -Mx']].max(axis=1)
        fig = go.Figure(data=[go.Bar(x=new_df['Support'], y=max_Mx, name='Maximum Mx')])
        fig.update_layout(
            title='Maximum Mx for each Support',
            xaxis_title='Support',
            yaxis_title='Maximum Mx (kNm)'
        )
        return fig

    elif option == 'Maximum My':
        max_My = new_df[['Max +My', 'Max -My']].max(axis=1)
        fig = go.Figure(data=[go.Bar(x=new_df['Support'], y=max_My, name='Maximum My')])
        fig.update_layout(
            title='Maximum My for each Support',
            xaxis_title='Support',
            yaxis_title='Maximum My (kNm)'
        )
        return fig

    elif option == 'Maximum Mz':
        max_Mz = new_df[['Max +Mz', 'Max -Mz']].max(axis=1)
        fig = go.Figure(data=[go.Bar(x=new_df['Support'], y=max_Mz, name='Maximum Mz')])
        fig.update_layout(
            title='Maximum Mz for each Support',
            xaxis_title='Support',
            yaxis_title='Maximum Mz (kNm)'
        )
        return fig

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
    
        }

        # Assign colors based on required_piles
        colors = required_piles.map(lambda x: color_map.get(x, 'gray'))  # Default color is gray for undefined mappings

        # Create Scatter plot
        fig = go.Figure(data=go.Scatter(
            x=new_df['X Coordinate'],
            y=new_df['Y Coordinate'],
            mode='markers',
            text=required_piles.astype(str),  # Convert to string for hover display
            marker=dict(
                size=12,
                color=colors,  # Use colors based on required piles
                line=dict(width=1, color='DarkSlateGrey')  # Marker line properties
            )
        ))

        fig.update_layout(
            title='Number of Piles required for each Support',
            xaxis_title='X Coordinate',  # Update with actual axis title
            yaxis_title='Y Coordinate',  # Update with actual axis title
            hovermode='closest'  # Display hover info closest to the mouse pointer
        )



        return fig

    else:
        raise ValueError(f"Invalid option {option}.")
