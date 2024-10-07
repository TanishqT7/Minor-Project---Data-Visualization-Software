import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class DataHandler():
    def __init__(self):
        self.data = None
        self.file_type = None

    def load_file(self, file_path: str):

        try:
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
                self.file_type = 'csv'

            elif file_path.endswith('.xlsx'):
                self.data = pd.read_excel(file_path)
                self.file_type = 'xlsx'

            else:
                raise ValueError(
                    "Unsupported file type, Please use a CSV or XLSX file.")

            self.validate_data()
            return self.data

        except Exception as e:
            raise ValueError(f"Error loading file: {e}")

    def validate_data(self):

        if self.data is None or self.data.empty:
            raise ValueError("No data found in the file.")

        if len(self.data.columns) < 2:
            raise ValueError("File must contain at least two columns.")

    def get_columns(self):

        if self.data is not None:
            return list(self.data.columns)
        else:
            raise ValueError("No data loaded.")

    def display_rows(self, num_rows: int):

        if self.data is None:
            raise ValueError("No data loaded!")

        if num_rows <= 0:
            raise ValueError("Please enter positive number of rows.")

        total_rows = min(num_rows, len(self.data))

        print(self.data.head(total_rows))

    def set_dependent_variable(self, var: str):

        if var not in self.get_columns():
            raise ValueError(f"{var} is not a valid column name")

        self.dependent_variable = var

        print(f"{var} is the dependent variable.")

    def set_independent_variable(self, vars: str):

        vars = vars.split(',') if "," in vars else [vars]

        vars = [var.strip() for var in vars]

        if not all(var in self.get_columns() for var in vars):
            raise ValueError(
                "One or more independent variables are not valid names")

        if self.dependent_variable in vars:
            raise ValueError(
                "Dependent variable cannot be an independent variable")

        self.independent_variable = vars
        print(f"The independent variables is/are: {vars}")

    def disp_sel_var(self):

        if self.dependent_variable is None:
            raise ValueError("Dependent variable not set.")

        if not self.independent_variable:
            raise ValueError("No independent variables set.")

        selected_vars = [self.dependent_variable] + self.independent_variable

        print(self.data[selected_vars].head(5))

    def handle_missing_values(self, strat="drop", fill_value=None):

        if strat == "drop":
            self.data = self.data.dropna()
        elif strat == "fill":
            if fill_value == "mean":
                self.data = self.data.fillna(self.data.mean())
            elif fill_value == "median":
                self.data = self.data.fillna(self.data.median())
            else:
                self.data = self.data.fillna(fill_value)
        else:
            raise ValueError("Unsupported missing data Strategy. Use \"Fill\" or \"Drop\".")
        
    def remove_duplicates(self):
        self.data = self.data.drop_duplicates()

    def normalize_data(self, columns=None):

        scaler = MinMaxScaler()
        if columns is None:
            self.data[self.data.select_dtypes(include=["float64", "int64"]).columns] = scaler.fit_transform(self.data.select_dtypes(include=["float64", "int64"]))

        else:
            self.data[columns] = scaler.fit_transform(self.data[columns])

    def standardize_data(self, columns=None):

        scaler = StandardScaler()
        if columns is None:
            self.data[self.data.select_dtypes(include=["float64", "int64"]).columns] = scaler.fit_transform(
                self.data.select_dtypes(include=["float64", "int64"]))

        else:
            self.data[columns] = scaler.fit_transform(self.data[columns])

    def encode_cat_variables(self, columns=None):

        if columns is None:
            self.data = pd.get_dummies(self.data)
        else:
            self.data = pd.get_dummies(self.data, columns=columns)

    def remove_outliers(self, z_thresh=3):

        from scipy import stats

        z_score = stats.zscore(self.data.select_dtypes(include=["float64", "int64"]))
        abs_z_score = abs(z_score)

        filtered_entries = (abs_z_score < z_thresh).all(axis=1)

        self.data = self.data[filtered_entries]