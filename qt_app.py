import sys
import visualization as vz
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QInputDialog,
    QDialog,
    QFormLayout,
    QListWidget,
    QListWidgetItem,
    QDialogButtonBox,
    QAbstractItemView,
    QFileDialog,
)
from data_handler import DataHandler


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualization Tool")
        self.setGeometry(100, 100, 1280, 720)

        self.handler = DataHandler()

        self.load_stylesheet('style.qss')

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.load_button = QPushButton("Load File", self)
        self.load_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_button)

        self.display_text = QTextEdit(self)
        layout.addWidget(self.display_text)

        self.sub_vars_button = QPushButton("Select Dependent and Independent Variables", self)
        self.sub_vars_button.clicked.connect(self.submit_variables)
        layout.addWidget(self.sub_vars_button)

        self.clean_button = QPushButton("Data Cleaning Options", self)
        self.clean_button.clicked.connect(self.data_cleaning_options)
        layout.addWidget(self.clean_button)

        self.visualize_button = QPushButton("Visualize Data", self)
        self.visualize_button.clicked.connect(self.visualize_data)
        layout.addWidget(self.visualize_button)

        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        # self.setLayout(layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_file(self):

        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Open CSV/XLSX File", "", "CSV Files (*.csv);; XLSX Files (*.xlsx);; All Files (*)", options=options
            )

            if file_name:
                self.handler.load_file(file_name)
                self.display_text.append(f"File Loaded from: {file_name}")
                self.display_columns()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_columns(self):

        try:
            columns = self.handler.get_columns()
            self.display_text.append(f"Columns Available: {columns}")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def submit_variables(self):

        try:
            columns = self.handler.get_columns()

            dialog = QDialog(self)
            dialog.setWindowTitle("Select Dependent and Independent Variables")
            layout = QVBoxLayout()

            dep_label = QLabel("Select Dependent Variables: ")
            layout.addWidget(dep_label)
            dep_combo = QComboBox(dialog)
            dep_combo.addItems(columns)
            layout.addWidget(dep_combo)

            indep_label = QLabel("Select Independent Variables: ")
            layout.addWidget(indep_label)
            indep_list = QListWidget(dialog)
            indep_list.setSelectionMode(QAbstractItemView.MultiSelection)
            for col in columns:
                item = QListWidgetItem(col)
                indep_list.addItem(item)
            layout.addWidget(indep_list)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:

                dep_var = dep_combo.currentText()

                indep_vars = [item.text() for item in indep_list.selectedItems()]

                if not indep_vars:
                    QMessageBox.critical(self, "Error", "Please select at least one independent variable")
                    return
                
                self.handler.set_dependent_variable(dep_var)
                self.handler.set_independent_variable(indep_vars)

                self.handler.disp_sel_var()

                if self.handler.usable_data is None or self.handler.usable_data.empty:
                    self.display_text.append("Data is empty or None")
                    return  

                self.display_text.append(f"Dependent Variable: {dep_var}")
                self.display_text.append(f"Independent Variables: {indep_vars}")

                self.disp_sele_var()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def disp_sele_var(self):

        if self.handler.usable_data is None or self.handler.usable_data.empty:
            QMessageBox.critical(self, "Error", "Usable Data is empty or None")
            return
        print(f"Avalaible Variables: {self.handler.usable_data.columns}")

        selec_var = [self.handler.dependent_variable] + \
            self.handler.independent_variable

        try:

            updated_vars = []

            for var in selec_var:
                if var in self.handler.usable_data.columns:
                    updated_vars.append(var)
                else:
                    dummy_vars = [col for col in self.handler.usable_data.columns if col.startswith(var + "_")]
                    updated_vars.extend(dummy_vars)

            self.usable_data_qt = self.handler.usable_data[updated_vars]

            print("Selected Variables: ", updated_vars)
            print("data Preview: \n", self.usable_data_qt.head())

            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)

            self.table_widget.setRowCount(len(self.usable_data_qt))
            self.table_widget.setColumnCount(len(updated_vars))
            self.table_widget.setHorizontalHeaderLabels(updated_vars)

            for r_idx, r_data in self.usable_data_qt.iterrows():
                for c_idx, c_data in enumerate(updated_vars):
                    self.table_widget.setItem(
                        r_idx, c_idx, QTableWidgetItem(str(r_data[c_data])))

            self.table_widget.viewport().update()

            row_count = self.table_widget.rowCount()
            for row_idx in range(row_count - 1, -1, -1):
                empty = True
                for col_idx in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row_idx, col_idx)
                    if item and item.text().strip():
                        empty = False
                        break
                if empty:
                    self.table_widget.removeRow(row_idx)

        except KeyError as e:
            QMessageBox.critical(
                self, "Error", f"Error Displaying selected variables: {e}")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error Displaying selected variables: {e}")
            print(f"Error Refreshing Table: {e}")

    def get_encoded_variables(self, dep_var, indep_var):
        if dep_var in self.handler.cat_cols:
            dep_var = self.get_encoded_column(dep_var)
        if indep_var in self.handler.cat_cols:
            indep_var = self.get_encoded_column(indep_var)

        return dep_var, indep_var
    
    def get_encoded_column(self, col):
        encoded_cols = [c for c in self.handler.usable_data.columns if c.startswith(col + "_")]
        return encoded_cols[0] if encoded_cols else None

    def data_cleaning_options(self):
        options = [
            "Handle Missing Data",
            "Remove Duplicates",
            "Normalize Data",
            "Standardize Data",
            "Encode Categorical Data",
            "Remove Outliers",
        ]

        choice, ok = QInputDialog.getItem(
            self, "Data Cleaning Options", "Select an Option: ", options, 0, False
        )

        if ok and choice:
            if choice == "Handle Missing Data":
                self.handle_missing_data()
            elif choice == "Remove Duplicates":
                self.remove_duplicates()
            elif choice == "Normalize Data":
                self.normalize_data()
            elif choice == "Standardize Data":
                self.standardize_data()
            elif choice == "Encode Categorical Data":
                self.encode_categorical_data()
            elif choice == "Remove Outliers":
                self.remove_outliers()

    def handle_missing_data(self):
        strat, ok = QInputDialog.getItem(
            self, "Handling Missing Data", "Choose Strategy: (Drop / Fill): ", [
                "drop", "fill"], 0, False
        )

        if ok:
            if strat == "fill":
                fill_value, ok_fill = QInputDialog.getText(
                    self, "Fill Value", "Enter Fill Value(mean / median / specific): "
                )
                if ok_fill:
                    self.handler.handle_missing_values(
                        strat="fill", fill_value=fill_value)
                    self.display_text.append(
                        f"Filled missing values using {fill_value}")
            elif strat == "drop":
                self.handler.handle_missing_values(strat="drop")
                self.display_text.append("Dropped missing values")

            print(self.handler.usable_data.head())
            self.disp_sele_var()

    def remove_duplicates(self):
        self.handler.remove_duplicates()
        self.display_text.append("Removed Duplicates")
        self.disp_sele_var()

    def normalize_data(self):

        try:
            numeric_columns = self.handler.get_numerical_columns()

            dep_var = self.handler.get_dependent_variable()
            if dep_var in numeric_columns:
                numeric_columns.remove(dep_var)

            dialog = QDialog(self)
            dialog.setWindowTitle("Select Columns to Normalize")
            layout = QVBoxLayout()

            label = QLabel("Select Columns to Normalize: ")
            layout.addWidget(label)

            columns_list = QListWidget(dialog)
            columns_list.setSelectionMode(QAbstractItemView.MultiSelection)
            for col in numeric_columns:
                item = QListWidgetItem(col)
                columns_list.addItem(item)
            layout.addWidget(columns_list)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                selected_columns = [item.text() for item in columns_list.selectedItems()]

                if not selected_columns:
                    selected_columns = None

                self.handler.normalize_data(columns=selected_columns)
                self.display_text.append("Data Normalized")
                self.disp_sele_var()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def standardize_data(self):
        
        try:
            numeric_columns = self.handler.get_numerical_columns()

            dep_var = self.handler.get_dependent_variable()
            if dep_var in numeric_columns:
                numeric_columns.remove(dep_var)

            dialog = QDialog(self)
            dialog.setWindowTitle("Select Columns to Standardize")
            layout = QVBoxLayout()

            label = QLabel("Select Columns to Standardize: ")
            layout.addWidget(label)

            columns_list = QListWidget(dialog)
            columns_list.setSelectionMode(QAbstractItemView.MultiSelection)
            for col in numeric_columns:
                item = QListWidgetItem(col)
                columns_list.addItem(item)
            layout.addWidget(columns_list)

            button_box = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                selected_columns = [item.text()
                                    for item in columns_list.selectedItems()]

                if not selected_columns:
                    selected_columns = None

                self.handler.standardize_data(columns=selected_columns)
                self.display_text.append("Data Standardized")
                self.disp_sele_var()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def encode_categorical_data(self):

        try:
            cat_columns = self.handler.get_categorical_columns()

            dep_var = self.handler.get_dependent_variable()
            if dep_var in cat_columns:
                cat_columns.remove(dep_var)

            dialog = QDialog(self)
            dialog.setWindowTitle("Select Categorical Variables to Encode")
            layout = QVBoxLayout()

            label = QLabel("Select Columns to Encode: ")
            layout.addWidget(label)

            columns_list = QListWidget(dialog)
            columns_list.setSelectionMode(QAbstractItemView.MultiSelection)
            for col in cat_columns:
                item = QListWidgetItem(col)
                columns_list.addItem(item)
            layout.addWidget(columns_list)

            button_box = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                selected_columns = [item.text()
                                    for item in columns_list.selectedItems()]

                if not selected_columns:
                    selected_columns = None

                self.handler.encode_cat_variables(columns=selected_columns)
                self.display_text.append("Categorical Data Encoded")
                self.disp_sele_var()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def remove_outliers(self):
        z_thresh, ok = QInputDialog.getDouble(
            self, "Remove Outliers", "Enter Z-Threshold for outliers: ", 3.0, 0.1, 10.0, 1
        )

        if ok:
            self.handler.remove_outliers(z_thresh=z_thresh)
            self.display_text.append("Outliers Removed")
            self.disp_sele_var()

    def visualize_data(self):
        try:

            columns = self.handler.get_columns()

            dialog = QDialog(self)
            dialog.setWindowTitle("Select Visualization Options")
            layout = QVBoxLayout()

            graph_label = QLabel("Select Graph Type: ")
            layout.addWidget(graph_label)
            graph_type_combo = QComboBox(dialog)
            graph_type_combo.addItems(["Bar Graph", "Histogram", "Box Plot", "Scatter Plot", "Count Plot", "Pie Chart", "Pair Plot", "Heatmap"])
            layout.addWidget(graph_type_combo)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                graph_type = graph_type_combo.currentText()

                numeric_columns = self.handler.get_numerical_columns()
                cat_columns = self.handler.get_categorical_columns()

                valid_columns = []
                if graph_type in ["Bar Graph", "Count Plot", "Pie Chart"]:
                    valid_columns = cat_columns
                if graph_type in ["Histogram", "Box Plot", "Scatter Plot"]:
                    valid_columns = numeric_columns
                if graph_type in ["Pair Plot", "Heatmap"]:
                    valid_columns = numeric_columns + cat_columns

                if not valid_columns:
                    QMessageBox.critical(
                        self, "Error", f"No valid columns found for {graph_type}"
                    )
                    return
                
                if graph_type in ["Pair Plot", "Heatmap"]:

                    if graph_type == "Pair Plot":
                        vz.plot_pair(data=self.handler.usable_data)
                        return
                    elif graph_type == "Heatmap":
                        vz.plot_heatmap(data=self.handler.usable_data)
                        return
                    else:
                        QMessageBox.critical(
                            self, "Error", f"Invalid graph type: {graph_type}"
                        )
                        return
                    

                dialog_indep = QDialog(self)
                dialog_indep.setWindowTitle("Select Independent Variable")
                layout_indep = QVBoxLayout()

                indep_label = QLabel("Select Independent Variable: ")
                layout_indep.addWidget(indep_label)
                indep_combo = QComboBox(dialog)
                indep_combo.addItems(valid_columns)
                layout_indep.addWidget(indep_combo)

                button_box_indep = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                button_box_indep.accepted.connect(dialog_indep.accept)
                button_box_indep.rejected.connect(dialog_indep.reject)
                layout_indep.addWidget(button_box_indep)

                dialog_indep.setLayout(layout_indep)

                if dialog_indep.exec_() == QDialog.Accepted:
                    indep_var = indep_combo.currentText()

                    if self.handler.is_encoded:
                        indep_var = self.get_encoded_column(indep_var)

                    if graph_type == "Bar Graph":
                        vz.plot_barplot(data=self.handler.usable_data, column=indep_var)
                    elif graph_type == "Histogram":
                        vz.plot_histogram(data=self.handler.usable_data, columns=indep_var)
                    elif graph_type == "Box Plot":
                        vz.plot_boxplot(data=self.handler.usable_data, x_col=indep_var)
                    elif graph_type == "Scatter Plot":
                        vz.plot_scatter(self.handler.usable_data, x_col=indep_var, y_col=self.handler.dependent_variable)
                    elif graph_type == "Count Plot":
                        vz.plot_count(self.handler.usable_data, column=indep_var)
                    elif graph_type == "Pie Chart":
                        vz.plot_piechart(data=self.handler.usable_data, column=indep_var)
                    else:
                        QMessageBox.critical(
                            self, "Error", f"Invalid graph type: {graph_type}"
                        )

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_stylesheet(self, file_name):
        try:
            with open(file_name, 'r') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Error: QSS file {file_name} not found!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = App()
    main_win.show()
    sys.exit(app.exec_())
