from pandas import DataFrame
from IPython.display import display
# Dictionary for conversions to minutes
time_dict = {
    "Minute": 1,
    "Hour": 60,
    "Day": 3600,
    "Week": 25200
}

# price x quantity = full price becomes full price
def price_to_int(price: str):
    price = price.split("=  ", 1)[1]
    price = int(price.replace(',', ''))
    return price

# %d time ago = %d
def time_to_int(time: str):
    time = time.split(" ", 2)
    if time[0] == 'Now':
        time = 0
    else:
        time = int(time[0]) * time_dict[time[1]]
    return int(time)

# data frame difference
def dataframe_difference(df1: DataFrame, df2: DataFrame, which=None):
    """Find rows which are different between two DataFrames."""
    # We remove the "time" columns to make sure we can see differences
    reduced1 = df1.drop(['Last Seen', 'Last Seen Minutes'], axis=1)
    reduced2 = df2.drop(['Last Seen', 'Last Seen Minutes'], axis=1)
    comparison_df = reduced1.merge(
        reduced2,
        indicator=True,
        how='outer'
    )
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    return diff_df

