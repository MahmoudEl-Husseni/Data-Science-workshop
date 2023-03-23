import os 
import argparse
import numpy as np
import pandas as pd
#--------------------------------------------

def level_1(df):
    # change the column names
    column_names = df.columns
    for i, name in enumerate(column_names):
        rand_inidices = np.random.randint(0, len(name), len(name) // 2)
        new_name = f'Column_{i+1}_'
        for index in range(len(name)):
            if index in rand_inidices:
                new_name += name[index].upper()
            else:
                new_name += name[index]
        

        df.rename(columns={name: new_name}, inplace=True)
    return df


def level_3(df, column1=None, column2=None, date_column=None, percentage=0.5, kind=1):
    '''
    kind values: 
    0 0 (0) -> no edit
    0 1 (1) -> MCAR only
    1 0 (2) -> MNAR only
    1 1 (3) -> MNAR & MCAR
    '''
    # Delete some random values in column1
    df_missing = df.copy()
    if kind%2:
        assert column1 is not None, "Column1 not provided"
        indices = np.arange(len(df))
        np.random.shuffle(indices)
        rand_indices = indices[:int(percentage * len(df))]
        for index in rand_indices:
            df_missing.loc[index, column1] = np.nan
    
    # delete some values in fixed periods
    if (kind//2):
        assert (column2 is not None) or (date_column is not None), "Column2 not provided"
        time_frame = pd.to_datetime(df[date_column])
        df['month'] = time_frame.dt.month
        df_missing['month'] = time_frame.dt.month
#         df['day'] = time_frame.dt.day
#         df['year'] = time_frame.dt.year
#         df['day_of_week'] = time_frame.dt.day_name()
        df_missing.loc[df['month']<10, 'wind_speed'] = np.nan

    return df_missing


if __name__ == '__main__':


    args = argparse.ArgumentParser()  
    args.add_argument('-i', '--input', type=str, default='../data/wuzzuf_DS.csv')
    args.add_argument('-o', '--output', type=str, default='../data/un_cleaned_data.csv')
    args.add_argument('-s', '--save', type=int, default=0)
    args.add_argument('-l', '--level', type=int, default=1)

    args = args.parse_args()

    df = pd.read_csv("../data/" + args.input)
    if args.level == 1:
        df = level_1(df)
    elif args.level == 3:
        df = level_3(df, column1='pressure', column2='wind_speed', date_column='date', percentage=0.5, kind=3)

    
    print(df.head())
    
    if args.save == 1:
        df.to_csv("../data/" + args.output, index=False)

    
