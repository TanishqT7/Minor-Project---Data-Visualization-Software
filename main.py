from data_handler import DataHandler


def main():

    handler = DataHandler()

    while True:
        try:
            file_path = ""

            while True:
                file_path = input("Enter the file path, or type exit to quit: ")

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
                    
                    disp_rows = int(input("Enter the number of rows to display: "))
                    handler.display_rows(disp_rows)
                    break
                except ValueError as e:
                    print(f"Invalid number of Rows: {e}")
            
            while True:
                try:
                    dep_var = input("Enter the name of the dependent variable: ")
                    handler.set_dependent_variable(dep_var)
                    break
                except ValueError as e:
                    print(f"Invalid input for Dependent Variable: {e}")

            while True:
                try:
                    indep_vars = input(
                        "Enter the names of the independent variables (comma-separated): ")
                    #indep_vars = [var.strip(',') for var in indep_vars]
                    handler.set_independent_variable(indep_vars)
                    break
                except ValueError as e:
                    print(f"Invalid input for Independent Variables: {e}")

            handler.disp_sel_var()

        except Exception as e:
            print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
