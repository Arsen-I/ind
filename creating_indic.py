import numpy as np


def func_ind(df):

    a1 = 0.00001
    b1 = 0.00005
    c1 = 0.00016
    d1 = 0.00733

    a2 = 0.00002
    b2 = 0.00017
    c2 = 0.00054
    d2 = 0.00859

    a3 = 0.00004
    b3 = 0.00078
    c3 = 0.00266
    d3 = 0.01161

    k_sj = 0.9

    df['ind_1'] = np.where(df['avg_month_temp'] <= 0,
                           (0.968 * (1 - df['avg_wind_speeds'] * (
                                   a1 * df['avg_month_temp'] ** 2 + b1 * df['avg_month_temp'] + c1) + d1 * df[
                                         'avg_month_temp'])),
                           (1 - df['n_t_div_n'] - df['n_rainfall_div_n'] + k_sj * df['n_t_div_n'] + (1 - 0.0388) * df[
                               'n_rainfall_div_n']))

    df['ind_1'] = round(df['ind_1'], 5)

    df['ind_2'] = np.where(df['avg_month_temp'] <= 0,
                           (0.968 * (1 - df['avg_wind_speeds'] * (
                                   a2 * df['avg_month_temp'] ** 2 + b2 * df['avg_month_temp'] + c2) + d2 * df[
                                         'avg_month_temp'])),
                           (1 - df['n_t_div_n'] - df['n_rainfall_div_n'] + k_sj * df['n_t_div_n'] + (1 - 0.0388) * df[
                               'n_rainfall_div_n']))
    df['ind_2'] = round(df['ind_2'], 5)

    df['ind_3'] = np.where(df['avg_month_temp'] <= 0,
                           (0.968 * (1 - df['avg_wind_speeds'] * (
                                   a3 * df['avg_month_temp'] ** 2 + b3 * df['avg_month_temp'] + c3) + d3 * df[
                                         'avg_month_temp'])),
                           (1 - df['n_t_div_n'] - df['n_rainfall_div_n'] + k_sj * df['n_t_div_n'] + (1 - 0.0388) * df[
                               'n_rainfall_div_n']))
    df['ind_3'] = round(df['ind_3'], 5)

    df['ind_4'] = np.where(df['avg_month_temp'] <= 0,
                           1,
                           (1 - df['n_t_div_n'] + k_sj * df['n_t_div_n']))
    df['ind_4'] = round(df['ind_4'], 5)

    df['ind_5'] = 1

    df.index = range(1, len(df) + 1)

    df.to_excel('df.xlsx')

    indic = df[['ind_1', 'ind_2', 'ind_3', 'ind_4', 'ind_5']].transpose()
    indic.reset_index(drop=True, inplace=True)

    return indic