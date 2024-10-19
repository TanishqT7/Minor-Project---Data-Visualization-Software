import analysis.visualization as vs

def univariate_analysis(handler):
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

def bivariate_analysis(handler, dep_var):
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

def multivariate_analysis(handler):
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

def categorical_analysis(handler):
    while True:

        if handler.is_encoded:
            print("Categorical Variables have been encoded")
            print("\nCategorical Analysis Options:")
            print("1. Bar Plot for Encoded Variables")
            print('2. Heatmap for Encoded Variables')
            print("3. Back to main Visualization Menu")

            choice = int(input("Enter you choice (1-3): "))

            if choice == 1:
                columns = [col for col in handler.new_cols if col]
                print(f"Encoded Columns: {columns}")
                col = input("Enter the name of encoded column: ")
                vs.plot_barplot(data=handler.usable_data, column=col)

            elif choice == 2:
                vs.plot_heatmap(data=handler.usable_data)

            elif choice == 3:
                print("Returning to main visualization menu.")
                break

            else:
                print("Invalid option. Please try again.")
        
        else:
            print("Categorical Variables are not encoded")
            print("\nCategorical Analysis Options:")
            print("1. Count Plot for Encoded Variables")
            print('2. Pie Chart for Encoded Variables')
            print("3. Back to main Visualization Menu")

            choice = int(input("Enter you choice (1-3): "))

            if choice == 1:
                columns = handler.get_categorical_columns()
                print(f"Categorical Columns: {columns}")
                col = input("Enter the name of categorical column: ")
                vs.plot_count(data=handler.usable_data, column=col)

            elif choice == 2:
                columns = handler.get_categorical_columns()
                print(f"Categorical Columns: {columns}")
                col = input("Enter the name of categorical column: ")
                vs.plot_piechart(data=handler.usable_data, column=col)

            elif choice == 3:
                print("Returning to main visualization menu.")
                break

            else:
                print("Invalid option. Please try again.")