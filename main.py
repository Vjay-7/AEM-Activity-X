import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                           QTableWidgetItem, QInputDialog, QMessageBox, QLineEdit,
                           QSpinBox, QDialog, QFormLayout)
from datetime import datetime

class ReservationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Make Reservation")
        self.setModal(True)
        
        layout = QFormLayout()
        
        # Create input fields
        self.name_input = QLineEdit()
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("HH:MM")
        
        self.adult_input = QSpinBox()
        self.children_input = QSpinBox()
        self.senior_input = QSpinBox()
        
        # Add fields to layout
        layout.addRow("Name:", self.name_input)
        layout.addRow("Date:", self.date_input)
        layout.addRow("Time:", self.time_input)
        layout.addRow("Number of Adults:", self.adult_input)
        layout.addRow("Number of Children:", self.children_input)
        layout.addRow("Number of Senior Citizens:", self.senior_input)
        
        # Add buttons
        buttons = QHBoxLayout()
        self.submit_btn = QPushButton("Submit")
        self.cancel_btn = QPushButton("Cancel")
        buttons.addWidget(self.submit_btn)
        buttons.addWidget(self.cancel_btn)
        
        layout.addRow(buttons)
        self.setLayout(layout)
        
        # Connect buttons
        self.submit_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
    
    def get_data(self):
        return {
            'name': self.name_input.text(),
            'date': self.date_input.text(),
            'time': self.time_input.text(),
            'adults': self.adult_input.value(),
            'children': self.children_input.value(),
            'seniors': self.senior_input.value()
        }

class RestaurantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.reserv_list = []
        self.res_no = 0
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Veejay's Buffet Restaurant")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add title
        title = QLabel("Welcome to Veejay's Buffet Restaurant")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Create buttons
        button_layout = QHBoxLayout()
        buttons = [
            ("View Reservations", self.view_reservations),
            ("Make Reservation", self.make_reservation),
            ("Delete Reservation", self.delete_reservation),
            ("Generate Report", self.generate_report)
        ]
        
        for text, slot in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            'Res No.', 'Name', 'Date', 'Time', 'No. of Adults',
            'No. Children', 'No. Senior Citizen', 'Total Guest', 'Total Amount'
        ])
        layout.addWidget(self.table)
        
    def update_table(self):
        self.table.setRowCount(len(self.reserv_list))
        for row, reservation in enumerate(self.reserv_list):
            for col, value in enumerate(reservation):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)
        self.table.resizeColumnsToContents()
    
    def view_reservations(self):
        self.update_table()
    
    def make_reservation(self):
        dialog = ReservationDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            # Validate inputs
            if not all([data['name'], data['date'], data['time']]):
                QMessageBox.warning(self, "Error", "Please fill in all fields")
                return
            
            try:
                datetime.strptime(data['date'], '%Y-%m-%d')
                datetime.strptime(data['time'], '%H:%M')
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid date or time format")
                return
            
            self.res_no += 1
            total_guest = data['adults'] + data['children'] + data['seniors']
            sub_total = (data['adults'] * 500) + (data['children'] * 250) + (data['seniors'] * 400)
            
            self.reserv_list.append([
                self.res_no, data['name'], data['date'], data['time'],
                data['adults'], data['children'], data['seniors'],
                total_guest, sub_total
            ])
            
            self.update_table()
            QMessageBox.information(self, "Success", "Reservation added successfully!")
    
    def delete_reservation(self):
        res_no, ok = QInputDialog.getInt(self, "Delete Reservation", 
                                       "Enter Reservation Number:", 1, 1, 999999)
        if ok:
            for i, reservation in enumerate(self.reserv_list):
                if reservation[0] == res_no:
                    del self.reserv_list[i]
                    self.update_table()
                    QMessageBox.information(self, "Success", 
                                          f"Reservation No. {res_no} deleted successfully")
                    return
            QMessageBox.warning(self, "Error", "Reservation not found")
    
    def generate_report(self):
        res_no, ok = QInputDialog.getInt(self, "Generate Report", 
                                       "Enter Reservation Number:", 1, 1, 999999)
        if ok:
            for reservation in self.reserv_list:
                if reservation[0] == res_no:
                    msg = f"""
Reservation Details:
-------------------
Reservation No.: {reservation[0]}
Name: {reservation[1]}
Date: {reservation[2]}
Time: {reservation[3]}
Adults (P500): {reservation[4]}
Children (P250): {reservation[5]}
Senior Citizens (P400): {reservation[6]}
Total Guests: {reservation[7]}
Total Amount: P{reservation[8]:.2f}
"""
                    QMessageBox.information(self, "Reservation Report", msg)
                    return
            QMessageBox.warning(self, "Error", "Reservation not found")

def main():
    app = QApplication(sys.argv)
    window = RestaurantApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()