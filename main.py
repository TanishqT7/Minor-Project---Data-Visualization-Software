from data_handler import DataHandler
import visualization as vs


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
                                        handler.handle_missing_values(
                                            strat="drop")
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
                                    handler.encode_cat_variables(
                                        columns=columns)
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
                                    handler.remove_outliers(
                                        z_thresh=z_threshold)
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

            while True:
                try:
                    print("\nData Visualization Options:")
                    print("1. Univariate Analysis")
                    print("2. Bivariate Analysis")
                    print("3. Multivariate Analysis")
                    print("4. Exit Visualization")

                    analysis_type = int(
                        input("Choose the type of analysis (1-4): "))

                    if analysis_type == 1:
                        while True:
                            print("\nUnivariate Analysis Options:")
                            print("1. Histogram")
                            print("2. Count Plot")
                            print("3. Back to main Visualization Menu")

                            univariate_options = int(
                                input("Enter you choice (1-3): "))

                            if univariate_options == 1:
                                column = input(
                                    "Enter the name of the column: ")
                                bins = int(input("Enter the number of bins: "))

                                vs.plot_histogram(
                                    data=handler.usable_data, columns=column, bins=bins)

                            elif univariate_options == 2:
                                column = input(
                                    "Enter the name of the column: ")
                                vs.plot_count(
                                    data=handler.usable_data, column=column)

                            elif univariate_options == 3:
                                print("Returning to main visualization menu.")
                                break

                            else:
                                print("Invalid option. Please try again.")

                    elif analysis_type == 2:
                        while True:
                            print("\nBivariate Analysis Options:")
                            print("1. Scatter Plot")
                            print("2. Box Plot")
                            print("3. Back to main Visualization Menu")

                            bivariate_options = int(
                                input("Enter you choice (1-3): "))

                            if bivariate_options == 1:
                                x_col = input(
                                    "Enter the name of the X-axis column: ")
                                y_col = dep_var
                                hue = input(
                                    "Enter the name of the Hue column (or press enter for no hue): ")
                                hue = hue if hue.strip() else None
                                vs.plot_scatter(
                                    data=handler.usable_data, x_col=x_col, y_col=y_col, hue=hue)

                            elif bivariate_options == 2:
                                x_col = input(
                                    "Enter the name of a Categorical column: ")
                                y_col = dep_var
                                vs.plot_boxplot(
                                    data=handler.usable_data, x_col=x_col, y_col=y_col)

                            elif bivariate_options == 3:
                                print("Returning to main visualization menu.")
                                break

                            else:
                                print("Invalid option. Please try again.")

                    elif analysis_type == 3:
                        while True:
                            print("\nMultivariate Analysis Options:")
                            print("1. Pair Plot")
                            print("2. Correlation Heatmap")
                            print("3. Back to main Visualization Menu")

                            multivariate_options = int(
                                input("Enter you choice (1-3): "))

                            if multivariate_options == 1:
                                hue = input(
                                    "Enter the name of the hue column (or press enter for no hue): ")
                                hue = hue if hue.strip() else None
                                vs.plot_pair(data=handler.usable_data, hue=hue)

                            elif multivariate_options == 2:
                                vs.plot_heatmap(data=handler.usable_data)

                            elif multivariate_options == 3:
                                print("Returning to main visualization menu.")
                                break

                            else:
                                print("Invalid option. Please try again.")

                    elif analysis_type == 4:
                        print("Exiting Visualization")
                        break

                    else:
                        print("Invalid option. Please try again.")

                    # plot_option = int(input("Enter your choice: "))

                    # if plot_option == 1:
                    #     x_col = input("Enter the name of the x-axis column: ")
                    #     y_col = input("Enter the name of the y-axis column: ")
                    #     hue = input(
                    #         "Enter the name of the hue column (or press enter for no hue): ")
                    #     title = input("Enter the title of the plot: ")

                    #     hue = hue if hue.strip() else None

                    #     plot_scatter(data=handler.usable_data, x_col=x_col, y_col=y_col, hue=hue, title=title)

                    # elif plot_option == 2:
                    #     columns = input("Enter the column to plot: ")
                    #     bins = int(input("Enter the number of bins: ") or 10)
                    #     plot_histogram(data=handler.usable_data, columns=columns, bins=bins)

                    # elif plot_option == 3:
                    #     x_col = input("Enter the name of the column to plot: ")
                    #     y_col = input("Enter the name of the y-axis column: ")

                    #     y_col = y_col if y_col.strip() else None

                    #     plot_boxplot(data=handler.usable_data, x_col=x_col, y_col=y_col)

                    # elif plot_option == 4:
                    #     print("Exiting Data Visualization steps.")
                    #     break

                    # else:
                    #     print("Invalid option. Please try again.")

                except ValueError as e:
                    print(f"Invalid input: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

        except Exception as e:
            print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()
