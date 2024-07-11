import pandas as pd
import plotly.graph_objs as go

def load_data(file_path):
    try:
        df_data = pd.read_excel(file_path, sheet_name='Foundation Reactions', skiprows=7, header=None)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

    if df_data.empty:
        raise ValueError("DataFrame is empty after reading the Excel file.")

    # Define meaningful column names based on your actual data structure
    column_names = ['Support', 'X Coordinate', 'Y Coordinate', 'Z Coordinate', 'TBR1', 'TBR2', 'TBR3', 'Combination', 'Fx [kN]', 'Fy [kN]', 'Fz [kN]', 'Mx [kNm]', 'My [kNm]', 'Mz [kNm]']
    
    # Rename columns
    df_data.columns = column_names
    
    # Drop unnecessary columns
    df_data.drop(columns=['TBR1', 'TBR2', 'TBR3'], inplace=True)

    # Drop last 7 rows
    df_data = df_data.iloc[:-7]

    # Forward fill first part
    df_data[['Support', 'X Coordinate', 'Y Coordinate', 'Z Coordinate']] = df_data[['Support', 'X Coordinate', 'Y Coordinate', 'Z Coordinate']].ffill()

    # Set index
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

def calculate_piles(safe_capacity, max_load):
    if safe_capacity <= 0:
        return 0
    return -(-max_load // safe_capacity)  # Ceiling division

def generate_plot(option, new_df, safe_pile_capacity=None, safe_pile_tensile_capacity=None):
    fig = go.Figure()

    # Always add number of piles if safe_pile_capacity is provided
    if safe_pile_capacity is not None:
        max_loads = new_df[['Max +Fz', 'Max -Fz']].apply(lambda x: x if x > 0 else 0, axis=1)
        required_piles = max_loads.apply(lambda x: calculate_piles(safe_pile_capacity, x))
        fig.add_trace(go.Bar(
            x=new_df['Support'],
            y=required_piles,
            name='Number of Piles',
            marker=dict(color='rgba(255, 0, 0, 0.5)')
        ))

    if option == 'Coordinates':
        unique_z_levels = new_df['Z Coordinate'].unique()

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

    elif option in ['Maximum Fx', 'Maximum Fy', 'Maximum Mx', 'Maximum My']:
        max_primary = new_df[f'Max +{option.split()[-1]}']
        max_secondary = new_df[f'Max -{option.split()[-1]}']
        fig.add_trace(go.Bar(
            x=new_df['Support'],
            y=max_primary,
            name=f'Maximum +{option.split()[-1]}',
            text=new_df[f'Max +{option.split()[-1]} Combination'],
            hoverinfo='text+y'
        ))
        fig.add_trace(go.Bar(
            x=new_df['Support'],
            y=max_secondary,
            name=f'Maximum -{option.split()[-1]}',
            text=new_df[f'Max -{option.split()[-1]} Combination'],
            hoverinfo='text+y'
        ))

        scatter_color = 'blue' if 'Fx' in option else 'green'  # Adjust scatter color based on option
        fig.add_trace(go.Scatter(
            x=new_df['Support'],
            y=new_df[f'Max +{option.split()[-1]}'],
            mode='markers',
            marker=dict(color=scatter_color),
            name=f'Max +{option.split()[-1]}',
            text=new_df[f'Max +{option.split()[-1]} Combination'],
            hoverinfo='text'
        ))
        fig.add_trace(go.Scatter(
            x=new_df['Support'],
            y=new_df[f'Max -{option.split()[-1]}'],
            mode='markers',
            marker=dict(color=scatter_color),
            name=f'Max -{option.split()[-1]}',
            text=new_df[f'Max -{option.split()[-1]} Combination'],
            hoverinfo='text'
        ))

        fig.update_layout(
            title=f'{option} for each Support',
            xaxis_title='Support',
            yaxis_title=f'{option} (kN or kNm)',
            barmode='relative'
        )

    elif option == 'Maximum Fz':
        max_Fz = new_df[['Max +Fz', 'Max -Fz']].max(axis=1)
        fig.add_trace(go.Bar(
            x=new_df['Support'],
            y=max_Fz,
            name='Maximum Fz',
            text=new_df['Max +Fz Combination'] + ' / ' + new_df['Max -Fz Combination'],
            hoverinfo='text+y'
        ))

        scatter_color = 'blue'  # Adjust scatter color as needed
        fig.add_trace(go.Scatter(
            x=new_df['Support'],
            y=new_df['Max +Fz'],
            mode='markers',
            marker=dict(color=scatter_color),
            name='Max +Fz',
            text=new_df['Max +Fz Combination'],
            hoverinfo='text'
        ))
        fig.add_trace(go.Scatter(
            x=new_df['Support'],
            y=new_df['Max -Fz'],
            mode='markers',
            marker=dict(color=scatter_color),
            name='Max -Fz',
            text=new_df['Max -Fz Combination'],
            hoverinfo='text'
        ))

        fig.update_layout(
            title='Maximum Fz for each Support',
            xaxis_title='Support',
            yaxis_title='Maximum Fz (kN)'
        )

    elif option == 'Maximum Mz':
        max_Mz = new_df[['Max +Mz', 'Max -Mz']].max(axis=1)
        fig.add_trace(go.Bar(
            x=new_df['Support'],
            y=max_Mz,
            name='Maximum Mz',
            text=new_df['Max +Mz Combination'] + ' / ' + new_df['Max -Mz Combination'],
            hoverinfo='text+y'
        ))

        scatter_color = 'green'  # Adjust scatter color as needed
        fig.add_trace(go.Scatter(
            x=new_df['Support'],
            y=new_df['Max +Mz'],
            mode='markers',
            marker=dict(color=scatter_color),
            name='Max +Mz',
            text=new_df['Max +Mz Combination'],
            hoverinfo='text'
        ))
        fig.add_trace(go.Scatter(
            x=new_df['Support'],
            y=new_df['Max -Mz'],
            mode='markers',
            marker=dict(color=scatter_color),
            name='Max -Mz',
            text=new_df['Max -Mz Combination'],
            hoverinfo='text'
        ))

        fig.update_layout(
            title='Maximum Mz for each Support',
            xaxis_title='Support',
            yaxis_title='Maximum Mz (kNm)'
        )

    else:
        raise ValueError(f"Invalid option {option}.")

    return fig