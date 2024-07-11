import pandas as pd
import plotly.graph_objs as go

def load_data(file_path):
    # Load the Excel file
    df_data = pd.read_excel(file_path, sheet_name='Foundation Reactions', skiprows=7, header=None)
    df_data.columns = ['Support', "X Coordinate", "Y Coordinate", "Z Coordinate", "TBR", "TBR", "TBR", "Combination", "Fx [kN]", "Fy [kN]", "Fz [kN]", "Mx [kNm]", "My [kNm]", "Mz [kNm]"]
    df_data.drop(df_data.columns[[4, 5, 6]], axis=1, inplace=True)
    df_data = df_data.iloc[:-7]

    # This method fills in the NaN in the merged cells.
    df_data_first_part = df_data.iloc[:, :4]
    df_data_rest = df_data.iloc[:, 4:]
    df_data_first_part = df_data_first_part.ffill(axis=0)
    df_data = pd.concat([df_data_first_part, df_data_rest], axis=1)

    # Create MultiIndex based on Support column
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
            print("Pile capacity is too low or too high")
            return

    if safe_pile_tensile_capacity != '':
        try:
            safe_pile_tensile_capacity = float(safe_pile_tensile_capacity)
            if safe_pile_tensile_capacity >= 0:
                print("Please enter a negative value for tensile capacity")
                return
        except ValueError:
            print("Invalid input for tensile capacity")
            return
    else:
        safe_pile_tensile_capacity = None

    if option == 'Number of Piles':
        new_df['Piles Required'] = new_df.apply(
            lambda row: max(
                calculate_piles(safe_pile_capacity, row['Max +Fz']),
                calculate_piles(safe_pile_tensile_capacity, abs(row['Max -Fz'])) if safe_pile_tensile_capacity else 0
            ),
            axis=1
        )

        over_capacity_supports = new_df[new_df['Piles Required'] > 6]['Support'].tolist()
        if over_capacity_supports:
            print(f"The number of piles exceeded 6 for the following supports: {', '.join(over_capacity_supports)}")
            return

        unique_z_levels = new_df['Z Coordinate'].unique()
        for z in unique_z_levels:
            df_z = new_df[new_df['Z Coordinate'] == z]
            trace = go.Scatter(
                x=df_z['X Coordinate'],
                y=df_z['Y Coordinate'],
                mode='markers+text',
                marker=dict(color='rgb(200,170,100)', size=10),
                text=df_z['Piles Required'].astype(str),
                hoverinfo='text',
                name=f'Support Points (Z={z})'
            )

            layout = go.Layout(
                title=f"(Z={z})",
                xaxis=dict(title='X Coordinate'),
                yaxis=dict(title='Y Coordinate'),
                showlegend=False
            )

            fig = go.Figure(data=[trace], layout=layout)
            fig.show()
    else:
        force_component_map = {
            'Maximum Fx': 'Fx',
            'Maximum Fy': 'Fy',
            'Maximum Fz': 'Fz',
            'Maximum Mx': 'Mx',
            'Maximum My': 'My',
            'Maximum Mz': 'Mz'
        }
        force_component = force_component_map[option]
        max_positive_col = f'Max +{force_component}'
        max_positive_comb_col = f'Max +{force_component} Combination'
        max_negative_col = f'Max -{force_component}'
        max_negative_comb_col = f'Max -{force_component} Combination'

        unique_z_levels = new_df['Z Coordinate'].unique()
        for z in unique_z_levels:
            df_z = new_df[new_df['Z Coordinate'] == z]
            trace = go.Scatter(
                x=df_z['X Coordinate'],
                y=df_z['Y Coordinate'],
                mode='markers',
                marker=dict(color='rgb(200,170,100)', size=10),
                text=df_z.apply(lambda row: f"Support: {row['Support']}<br>"
                                            f"Max +{force_component}: {row[max_positive_col]}<br>"
                                            f"+{force_component} Comb: {row[max_positive_comb_col]}<br>"
                                            f"Max -{force_component}: {row[max_negative_col]}<br>"
                                            f"-{force_component} Comb: {row[max_negative_comb_col]}",
                                axis=1),
                hoverinfo='text',
                name=f'Support Points (Z={z})'
            )

            layout = go.Layout(
                title=f"Support Forces Visualization (Z={z})",
                xaxis=dict(title='X Coordinate'),
                yaxis=dict(title='Y Coordinate'),
                showlegend=False
            )

            fig = go.Figure(data=[trace], layout=layout)
            fig.show()
