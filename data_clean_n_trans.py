def handle_missing_values(handler):
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
                        print(f"Filled the missing values using {fill_value}!")
                        break
                    else:
                        handler.handle_missing_values(
                            strat="fill", fill_value=float(fill_value))
                        print(
                            f"Filled the missing values using {fill_value}!")
                        break
                elif strat == "drop":
                    handler.handle_missing_values(
                        strat="drop")
                    print("Dropped the missing values!")
                    break
                else:
                    print("Invalid input. Please enter 'drop' or 'fill'.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def remove_duplicates(handler):
    handler.remove_duplicates()
    print("Handled duplicates successfully!")

def normalize_data(handler):
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

def standardize_data(handler):
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

def encode_categorical_data(handler):
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
                handler.encode_cat_variables(
                    columns=columns)
                print("Data Encoded")
                break
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def remove_outliers(handler):
    while True:
        try:
            z_threshold = float(
                input("Enter the z threshold to remove outliers, (Default is 3): ") or 3)
            if z_threshold == "exit":
                print("Exited Removing Outliers!")
                break
            else:
                handler.remove_outliers(
                    z_thresh=z_threshold)
                print(
                    f"Outliers removed with Z Threshold {z_threshold}")
                break
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def disp_data(handler):
    while True:
        try:
            handler.display_usable_data()
            break
        except ValueError as e:
            print(f"Invalid number of Rows: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
