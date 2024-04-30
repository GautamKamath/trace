import pandas as pd
import uuid

def run(dataset: pd.DataFrame, dimensions, measures, measure_fn, measure_name, threshold = 0):
    """
    Call this generic method to get the combination of the dimensional values and write to a csv value
    :param dataset: The dataset to run the combination code on
    :param dimensions: The list of columns to slice the dataset on
    :param measures: The list of columns on which to perform the measure function
    :param measure_fn: user defined function to execute on the measure columns
    :param measure_name: computed measure column name
    :param threshold: threshold to meet on the minimum number of rows for each combination
    """
    dim_unique_values = dict()
    for dim in dimensions:
        dim_unique_values[dim] = dataset[dim].unique()

    slim_dataset = dataset[dimensions + measures]

    result_dataset = []
    combinations(
        slim_dataset,
        dimensions,
        dim_unique_values,
        measures,
        measure_fn,
        measure_name,
        threshold,
        result_dataset)

    res_df = pd.DataFrame(result_dataset)
    res_df = res_df[[col for col in res_df if col != measure_name] + [measure_name]]
    res_df.to_csv("../resources/output-" + str(uuid.uuid4()) + ".csv")

def combinations(
        dataset: pd.DataFrame,
        dimensions,
        dim_unique_vals,
        measures,
        measure_fn,
        measure_name,
        row_threshold,
        result_dataset = [],
        dimensions_sliced = []):
    # If control reaches here we have all the dimensions sliced. Proceed with
    # calculating the measure and adding to the result dataset
    if len(dimensions) == 0:
        measure_and_report(
            dataset,
            measures,
            measure_name,
            measure_fn,
            result_dataset,
            dimensions_sliced)
        return

    dim = dimensions[0]
    # Boolean variable to ignore recursive call
    skippedOnce = False
    for dim_val in dim_unique_vals[dim]:
        filter_df = dataset[dataset[dim] == dim_val]
        # If true, no need to slice further. Proceed with calculating the measure
        # and adding to the result dataset
        if len(filter_df.index) < row_threshold:
            if not skippedOnce:
                combinations(
                    dataset,
                    dimensions[1:],
                    dim_unique_vals,
                    measures,
                    measure_fn,
                    measure_name,
                    row_threshold,
                    result_dataset,
                    dimensions_sliced)
                skippedOnce = True
        else:
            dimensions_sliced.append((dim, dim_val))
            combinations(
                filter_df,
                dimensions[1:],
                dim_unique_vals,
                measures,
                measure_fn,
                measure_name,
                row_threshold,
                result_dataset,
                dimensions_sliced)
            dimensions_sliced.pop()

def measure_and_report(
        dataset: pd.DataFrame,
        measures,
        measure_name,
        measure_fn,
        result_dataset,
        dimensions_sliced):
    result = measure_fn(dataset[measures])
    dimensions_sliced.append((measure_name, result))
    dim_dict = dict()
    for d, d_val in dimensions_sliced:
        dim_dict.update({d: d_val})
    result_dataset.append(dim_dict)
    dimensions_sliced.pop()