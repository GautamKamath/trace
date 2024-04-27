import uuid
import pandas as pd
import heapq

def sort_dimensions(dataset: pd.DataFrame, dimensions):
    sorted_dimensions = []
    for dim in dimensions:
        heapq.heappush(sorted_dimensions, (dataset[dim].nunique(), dim))
    sorted_dimensions = [item[1] for item in sorted_dimensions]
    return sorted_dimensions


def run(dataset: pd.DataFrame, dimensions, measures, measure_fn, measure_name, threshold = 0, best_effort=False):
    sorted_dimensions=dimensions
    if best_effort:
        sorted_dimensions = sort_dimensions(dataset, dimensions)

    slim_dataset = dataset[sorted_dimensions + measures]
    dim_unique_values = dict()
    for dim in dimensions:
        dim_unique_values[dim] = dataset[dim].unique()

    result_dataset = []
    combinations(
        slim_dataset,
        sorted_dimensions,
        dim_unique_values,
        measures,
        measure_fn,
        measure_name,
        100,
        result_dataset)

    res_df = pd.DataFrame(result_dataset)
    res_df.to_csv("../resources/output" + str(uuid.uuid4()) + ".csv")

def combinations(
        dataset: pd.DataFrame,
        dimensions,
        dim_unique_vals,
        measures,
        measure_fn,
        measure_name,
        row_threshold,
        result_dataset = [],
        dimensions_sliced = [],
        cache={}):
    # If control reaches here we have all the dimensions sliced. Proceed with
    # calculating the measure and adding to the result dataset
    if len(dimensions) == 0:
        cache_key = get_cache_key(dimensions_sliced)
        if cache_key not in cache:
            cache[cache_key] = True
            measure_and_report(
                dataset,
                measures,
                measure_name,
                measure_fn,
                result_dataset,
                dimensions_sliced)
        return

    dim = dimensions[0]
    skippedOnce = False
    for dim_val in dim_unique_vals[dim]:
        filter_df = dataset[dataset[dim] == dim_val]
        # If true, no need to slice further. Proceed with calculating the measure
        # and adding to the result dataset
        if len(filter_df.index) <= row_threshold:
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
                    dimensions_sliced,
                    cache)
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
                dimensions_sliced,
                cache)
            dimensions_sliced.pop()

def get_cache_key(dimensions_sliced):
    return "|".join(list(map(lambda x: str(x[1]), dimensions_sliced)))

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