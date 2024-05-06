The project consists of two files
1. eval_dataset.py
    - This is the generic algorithm which would be applicable for any dataset
    - To run the combination algorithm on any dataset, the following needs to be called<br>
      ```
          run(
              <pandas dataset>, 
              <list of dimension columns>
              <list of measures columns>
              <the function which calculates the output using the measure columns eg. ratio>,
              <the output column name>,
              <threshold used to skip dimensions if total rows are below this value>,
              <best effort which tries to maximize the number of combinations)
      ```
    - This algorithm 
      - recursively iterates through the `dimensions` list
      - for every dimension value combination, calculates the total rows in the dataset
      - if total rows is greater than threshold, adds the dimension in the current combination list
      - once all dimensions are exhausted, runs the user provided measure function
      - adds the new combination into the result dataset
      - if total rows is less than threshold, then skips the current dimension 
      
2. mortality_dataset.py
    - This is the real world dataset provided in the problem
    - Reads both the `women.csv` and `household.csv` files
    - Joins the two using the `cluster number` and `household number` columns
    - Calls the run method in the eval_dataset.


To run the real world problem, please run `python3 mortality_dataset.py`. The output 
should be created in the resources directory in the format output-<uuid>.csv. This will 
have all the combinations for the provided given input `dataset`, `dimensions` and `measures` 