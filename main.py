from data_handler import DataHandler


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
                        while True:
                            try:
                                strat = input(
                                    "How would you like to handle missing values? (drop or fill): ")
                                if strat == "exit":
                                    print("Exited Handling Missing Values!")
                                    break
                                else:
                                    if strat == "fill":
                                        fill_value = input(
                                            "Enter the Fill value ('mean', 'median', or specific value): ")
                                        if fill_value in ['mean', 'median']:
                                            handler.handle_missing_values(
                                                strat="fill", fill_value=fill_value)
                                            break
                                        else:
                                            handler.handle_missing_values(
                                                strat="fill", fill_value=float(fill_value))
                                            break
                                    else:
                                        handler.handle_missing_values(strat="drop")
                                        print("Dropped the missing values!")
                                        break
                            except ValueError as e:
                                print(f"Invalid input: {e}")
                            except Exception as e:
                                print(f"Unexpected error: {e}")

                    elif option == 2:

                        handler.remove_duplicates()
                        print("Handled duplicates successfully!")

                    elif option == 3:
                        while True:
                            try:
                                columns = input(
                                    "Enter the columns to normalize (comma-separated), or press Enter for all numeric columns: ")
                                if columns == "exit":
                                    print("Exited Normalizing Data!")
                                    break
                                else:
                                    columns = columns.split(
                                        ',') if columns else None
                                    columns = [col.strip() for col in columns]
                                    handler.normalize_data(columns=columns)
                                    print("Data Normalized")
                                    break
                            except ValueError as e:
                                print(f"Invalid input: {e}")
                            except Exception as e:
                                print(f"Unexpected error: {e}")

                    elif option == 4:
                        while True:
                            try:
                                columns = input(
                                    "Enter the columns to standardize (comma-separated), or press Enter for all numeric columns: ")
                                if columns == "exit":
                                    print("Exited Standardizing Data!")
                                    break
                                else:
                                    columns = columns.split(
                                        ',') if columns else None
                                    columns = [col.strip() for col in columns]
                                    handler.standardize_data(columns=columns)
                                    print("Data Standardized")
                                    break
                            except ValueError as e:
                                print(f"Invalid input: {e}")
                            except Exception as e:
                                print(f"Unexpected error: {e}")

                    elif option == 5:
                        while True:
                            try:
                                columns = input(
                                    "Enter the columns to encode (comma-separated), or press Enter for all categorical columns: ")
                                if columns == "exit":
                                    print("Exited Encoding Data!")
                                    break
                                else:
                                    columns = columns.split(
                                        ',') if columns else None
                                    columns = [col.strip() for col in columns]
                                    handler.encode_cat_variables(columns=columns)
                                    print("Data Encoded")
                                    break
                            except ValueError as e:
                                print(f"Invalid input: {e}")
                            except Exception as e:
                                print(f"Unexpected error: {e}")

                    elif option == 6:
                        while True:
                            try:
                                z_threshold = float(
                                    input("Enter the z threshold to remove outliers, (Default is 3): ") or 3)
                                if z_threshold == "exit":
                                    print("Exited Removing Outliers!")
                                    break
                                else:
                                    handler.remove_outliers(z_thresh=z_threshold)
                                    print(
                                        f"Outliers removed with Z Threshold {z_threshold}")
                                    break
                            except ValueError as e:
                                print(f"Invalid input: {e}")
                            except Exception as e:
                                print(f"Unexpected error: {e}")

                    elif option == 7:
                        while True:
                            try:
                                handler.display_usable_data()
                                break
                            except ValueError as e:
                                print(f"Invalid number of Rows: {e}")
                            except Exception as e:
                                print(f"Unexpected error: {e}")

                    elif option == 8:

                        print("Exiting Cleaning and Transforming steps.")
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
