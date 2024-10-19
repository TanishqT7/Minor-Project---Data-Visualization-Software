from data.data_handler import DataHandler
import data.data_clean_n_trans as dct
import analysis.visual_opts as vo

def main():

    handler = DataHandler()

    while True:
        try:
            file_path = ""

            while True:
                file_path = input(
                    "Enter the file path, or type exit to quit: ")

                if file_path.lower() == "exit":
                    print("Exiting the program!")
                    return

                try:
                    data = handler.load_file(file_path)
                    print("Data loaded successfully!")
                    break
                except ValueError as e:
                    print(f"Error Loading File: {e}")
                except Exception as e:
                    print(f"Unexpected Error: {e}")

            while True:
                try:
                    columns = handler.get_columns()
                    print("Columns Available: ", columns)

                    disp_rows = int(
                        input("Enter the number of rows to display: "))
                    handler.display_rows(disp_rows)
                    break
                except ValueError as e:
                    print(f"Invalid number of Rows: {e}")

            while True:
                try:
                    dep_var = input(
                        "Enter the name of the dependent variable: ")
                    handler.set_dependent_variable(dep_var)
                    break
                except ValueError as e:
                    print(f"Invalid input for Dependent Variable: {e}")

            while True:
                try:
                    indep_vars = input(
                        "Enter the names of the independent variables (comma-separated): ")
                    # indep_vars = [var.strip(',') for var in indep_vars]
                    handler.set_independent_variable(indep_vars)
                    break
                except ValueError as e:
                    print(f"Invalid input for Independent Variables: {e}")

            handler.disp_sel_var()

            while True:

                try:
                    print("\nData Cleaning and Transformation Options:")
                    print("1. Handle Missing Values")
                    print("2. Remove Duplicates")
                    print("3. Normalize Data")
                    print("4. Standardize Data")
                    print("5. Encode Categorical Data")
                    print("6. Remove Outliers")
                    print("7. Display Current Data")
                    print("8. Continue to the Next Step")

                    option = int(input("Enter you choice (1-8): "))

                    if option == 1:
                        dct.handle_missing_values(handler)

                    elif option == 2:
                        dct.remove_duplicates(handler)

                    elif option == 3:
                        dct.normalize_data(handler)

                    elif option == 4:
                        dct.standardize_data(handler)

                    elif option == 5:
                        dct.encode_categorical_data(handler)

                    elif option == 6:
                        dct.remove_outliers(handler)

                    elif option == 7:
                        dct.disp_data(handler)

                    elif option == 8:

                        print("Exiting Cleaning and Transforming steps.")
                        break

                    else:
                        print("Invalid option. Please try again.")

                except ValueError as e:
                    print(f"Invalid input: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

            while True:
                try:
                    print("\nData Visualization Options:")
                    print("1. Univariate Analysis")
                    print("2. Bivariate Analysis")
                    print("3. Multivariate Analysis")
                    print("4. Categorical Variables Analysis")
                    print("5. Exit Visualization")

                    analysis_type = int(
                        input("Choose the type of analysis (1-5): "))

                    if analysis_type == 1:
                        vo.univariate_analysis(handler)

                    elif analysis_type == 2:
                        vo.bivariate_analysis(handler, dep_var)

                    elif analysis_type == 3:
                        vo.multivariate_analysis(handler)

                    elif analysis_type == 4:
                        vo.categorical_analysis(handler)

                    elif analysis_type == 5:
                        print("Exiting Visualization")
                        break

                    else:
                        print("Invalid option. Please try again.")

                except ValueError as e:
                    print(f"Invalid input: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

        except Exception as e:
            print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()
