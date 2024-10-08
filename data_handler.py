import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class DataHandler():
    def __init__(self):
        self.main_data = None
        self.usable_data = None
        self.file_type = None
        self.dependent_variable = None
        self.independent_variable = []

    def load_file(self, file_path: str):

        try:
            if file_path.endswith('.csv'):
                self.main_data = pd.read_csv(file_path)
                self.file_type = 'csv'

            elif file_path.endswith('.xlsx'):
                self.main_data = pd.read_excel(file_path)
                self.file_type = 'xlsx'

            else:
                raise ValueError(
                    "Unsupported file type, Please use a CSV or XLSX file.")

            self.validate_data()
            return self.main_data

        except Exception as e:
            raise ValueError(f"Error loading file: {e}")

    def validate_data(self):

        if self.main_data is None or self.main_data.empty:
            raise ValueError("No data found in the file.")

        if len(self.main_data.columns) < 2:
            raise ValueError("File must contain at least two columns.")

    def get_columns(self):

        if self.main_data is not None:
            return list(self.main_data.columns)
        else:
            raise ValueError("No data loaded.")

    def display_rows(self, num_rows: int):

        if self.main_data is None:
            raise ValueError("No data loaded!")

        if num_rows <= 0:
            raise ValueError("Please enter positive number of rows.")

        total_rows = min(num_rows, len(self.main_data))

        print(self.main_data.head(total_rows))

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
        self.usable_data = self.main_data[selected_vars].copy()
        print(self.usable_data.head(5))

    def handle_missing_values(self, strat="drop", fill_value=None):

        if strat == "drop":
            self.usable_data.dropna(inplace=True)
        elif strat == "fill":
            if fill_value == "mean":
                self.usable_data.fillna(self.usable_data.mean(), inplace=True)
            elif fill_value == "median":
                self.usable_data.fillna(self.usable_data.median(), inplace=True)
            else:
                self.usable_data.fillna(fill_value, inplace=True)
        else:
            raise ValueError("Unsupported missing data Strategy. Use \"Fill\" or \"Drop\".")
        
    def remove_duplicates(self):
        self.usable_data.drop_duplicates(inplace=True)

    def normalize_data(self, columns=None):

        scaler = MinMaxScaler()
        if columns is None:
            norm_cols = self.usable_data.select_dtypes(
                include=["float64", "int64"]).columns

        else:
            norm_cols = columns
        scaled_data = scaler.fit_transform(self.usable_data[norm_cols])
        self.usable_data[norm_cols] = pd.DataFrame(scaled_data, columns=norm_cols, index=self.usable_data.index)

    def standardize_data(self, columns=None):

        scaler = StandardScaler()
        if columns is None:
            stand_cols = self.usable_data[self.usable_data.select_dtypes(include=["float64", "int64"]).columns]

        else:
            stand_cols = columns
        scaled_data = scaler.fit_transform(self.usable_data[stand_cols])
        self.usable_data[stand_cols] = pd.DataFrame(scaled_data, columns=stand_cols, index=self.usable_data.index)

    def encode_cat_variables(self, columns=None):

        self.usable_data = pd.get_dummies(self.usable_data, columns=columns)

    def remove_outliers(self, z_thresh=3):

        from scipy import stats
        
        num_cols = self.usable_data.select_dtypes(include=["float64", "int64"])
        z_score = stats.zscore(num_cols)
        abs_z_score = abs(z_score)

        filtered_entries = (abs_z_score < z_thresh).all(axis=1)

        self.usable_data = self.usable_data[filtered_entries]

    def display_usable_data(self):
        print(self.usable_data.head())