def enhance_summary(dataframe, custom_percentiles=[]):
    summary = dataframe.describe().T
    summary['IQR'] = summary['75%'] - summary['25%']
    summary['LW'] = summary['25%'] - 1.5 * summary['IQR']
    summary['UW'] = summary['75%'] + 1.5 * summary['IQR']

    for percentile in custom_percentiles:
        col_name = f'{percentile}%'
        # Calculate custom percentiles for each numeric column, handling NaN values
        for column in dataframe.select_dtypes(include=np.number).columns:
            value = np.nanpercentile(dataframe[column], percentile)
            summary.loc[column, col_name] = value

    # Calculate and add the count of outliers
    for column in dataframe.select_dtypes(include=np.number).columns:
        lower_range = summary.loc[column, 'LW']
        upper_range = summary.loc[column, 'UW']
        outliers = (dataframe[column] < lower_range) | (dataframe[column] > upper_range)
        num_outliers = np.sum(outliers)
        summary.loc[column, 'Outliers'] = num_outliers

    # Add the number of duplicates and missing values
    for column in dataframe.columns:
        summary.loc[column, 'Duplicates'] = dataframe[column].duplicated().sum()
        summary.loc[column, 'Missing'] = dataframe[column].isnull().sum()

    # Add skewness column and skewness category column
    for column in dataframe.select_dtypes(include=np.number).columns:
        skew_value = dataframe[column].skew()
        summary.loc[column, 'Skew'] = round(skew_value, 2)

        if skew_value >= 1:
            summary.loc[column, 'Skew_Category'] = 'Positive'
        elif skew_value <= -1:
            summary.loc[column, 'Skew_Category'] = 'Negative'
        elif -0.5 <= skew_value <= 0.5:
            summary.loc[column, 'Skew_Category'] = 'Normal'
        else:
            summary.loc[column, 'Skew_Category'] = 'Undefined'

    return summary
