from data_handler import DataHandler


def main():

    handler = DataHandler()

    while True:
        try:

            file_path = input("Enter the file path, or type exit to quit: ")

            if file_path.lower() == "exit":
                print("Exiting the program!")
                break

            data = handler.load_file(file_path)
            print("Data loaded successfully!")

            columns = handler.get_columns()
            print("Columns Available: ", columns)
            
            disp_rows = int(input("Enter the number of rows to display: "))
            handler.display_rows(disp_rows)

            dep_var = input("Enter the name of the dependent variable: ")
            handler.set_dependent_variable(dep_var)

            indep_vars = input(
                "Enter the names of the independent variables (comma-separated): ")
            #indep_vars = [var.strip(',') for var in indep_vars]
            handler.set_independent_variable(indep_vars)

            handler.disp_sel_var()

        except ValueError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
