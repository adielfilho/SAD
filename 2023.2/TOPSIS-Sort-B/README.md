# Topsis Sort B

 The TOPSIS-Sort-B is an enhanced variation of the TOPSIS-Sort method, designed to address classification and sorting problems in multiple criteria decision-making. In this method, boundary profiles are employed to determine categorization classes and to sort alternatives based on the proximity of their proximity coefficients to the established profiles.

## Technologies
| Technologies | Version | Install                               |
|--------------|---------|---------------------------------------|
| Python       | 3.12.1  | `pip install python==3.12.1`          |
| Numpy        | 1.26.4  | `pip install numpy==1.26.4`           |
| Pandas       | 2.2.1   | `pip install pandas==2.2.1`           |
| Streamlit    | 1.32.1  | `pip install streamlit==1.32.1`       |

## Installation
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a venv `python -m venv venv`
4. Activate the env `venv/Scripts/Activate (in windows)` or `source venv/bin/activate (in linux)`
5. Install the required dependencies by running the following command: `pip install -r requirements.txt`
## How to Run the Application
1. Ensure that you have the necessary dependencies installed.
2. Open a terminal or command prompt.
3. Navigate to the project directory.
4. Run the following command to start the application:
    ````
      cd src 
      cd main
      streamlit run main.py
   ```` 
5. The application will be launched in your default browser [URL](http://localhost:8501).

## How to Use

1. **Upload Your CSV File:**
   - You'll see a screen to upload your CSV file containing the required data. (A test entry can be found at ./src/files)
2. **Select the Dominant Profile:** 
   - After uploading the file, you'll be prompted to select the relevant dominant profile for analysis.
3. **Specify the Number of Values in the Domain Matrix:**
   - You'll need to input the desired number of values to compose the domain matrix.
4. **Provide the Number of Weights:**
   - Next, you'll be asked to input the number of weights needed for analysis.
5. **Assign Weights to Dominant Profiles:**
   - You'll be prompted to assign a weight to each selected dominant profile.
After completing these steps, the system will be ready to process and analyze the data according to your specifications.

## References

- Silva, D. F. L., & Filho, A. T. A. (2020). Sorting with TOPSIS through boundary and characteristic profiles. Journal Name, Volume(1), 141.
- GeeksforGeeks.TOPSIS method for Multiple-Criteria Decision Making (MCDM). Retrieved from [[URL](https://www.geeksforgeeks.org/topsis-method-for-multiple-criteria-decision-making-mcdm/)]

## Deploy
- Aplicação [Streamlit](https://topsis-sort-b-vgccjx9qm7l8j6tukepdvn.streamlit.app)
- Library [URL](https://pypi.org/project/TOPSIS-Sort-B/)

