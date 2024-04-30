import pandas as pd
import time
from eval_dataset import run

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

def prep_dataset():
    women_df = pd.read_csv("../resources/women.csv", index_col=0)
    household_df = pd.read_csv("../resources/household.csv").set_index(['Cluster number', 'Household number'])
    household_df.drop(axis='columns', columns=household_df.columns[0], inplace=True)
    final_df = women_df.join(household_df,
            on=['Cluster number', 'Household number'],
            how='inner',
            lsuffix='_women',
            rsuffix='_household')
    return final_df


def ratio(dataset: pd.DataFrame) -> float:
    sum_df = dataset.sum()
    if (sum_df['Total children ever born'] == 0):
        return 0.0
    return (sum_df['Sons who have died'] + sum_df['Daughters who have died']) / sum_df['Total children ever born']


if __name__ == '__main__':
    start = round(time.time())
    final_dataset = prep_dataset()
    dimensions = [
        "Age in 5-year groups",
        "Type of place of residence",
        "Number of household members",
        "Source of drinking water",
        "Time to get to water source (minutes)",
        "Type of toilet facility",
        "Has electricity",
        "Has radio",
        "Age of head of household",
    ]
    measures = [
        "Sons who have died",
        "Daughters who have died",
        "Total children ever born"
    ]
    final_dataset.filter(dimensions + measures).to_csv("../resources/input_join.csv")

    run(final_dataset, dimensions, measures, ratio, "under-5 mortality", threshold=10)
    end = round(time.time())
    print("Total Time: " + str((end - start)))