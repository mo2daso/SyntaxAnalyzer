from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout,
                           QTextEdit, QPushButton, QLabel,
                           QTabWidget, QTableWidget, QWidget)
from PyQt5.QtGui import QFont

def create_input_section(window):
    """Create the input section of the GUI"""
    input_frame = QFrame()
    input_frame.setFrameStyle(QFrame.StyledPanel)
    input_layout = QVBoxLayout(input_frame)
    
    input_label = QLabel("Enter Code:")
    input_label.setFont(QFont("Arial", 12, QFont.Bold))
    
    window.input_text = QTextEdit()
    window.input_text.setPlaceholderText("Example: x = 2 * (3 + 4)")
    window.input_text.setFixedHeight(150)
    
    button_layout = QHBoxLayout()
    window.analyze_btn = QPushButton("Analyze Code")
    window.analyze_btn.clicked.connect(window.analyze_code)
    window.clear_btn = QPushButton("Clear")
    window.clear_btn.clicked.connect(window.clear_all)
    window.exit_btn = QPushButton("Exit")
    window.exit_btn.clicked.connect(window.close)
    
    button_layout.addWidget(window.analyze_btn)
    button_layout.addWidget(window.clear_btn)
    button_layout.addWidget(window.exit_btn)
    
    input_layout.addWidget(input_label)
    input_layout.addWidget(window.input_text)
    input_layout.addLayout(button_layout)
    
    return input_frame

def create_results_section(window):
    """Create the results section of the GUI"""
    results_tab = QTabWidget()
    
    # Token analysis tab
    window.token_table = QTableWidget()
    window.token_table.setColumnCount(4)
    window.token_table.setHorizontalHeaderLabels(["Type", "Value", "Position", "Line"])
    results_tab.addTab(window.token_table, "Token Analysis")
    
    # Parse tree tab
    window.tree_widget = QWidget()
    window.tree_layout = QVBoxLayout(window.tree_widget)
    results_tab.addTab(window.tree_widget, "Parse Tree")
    
    # Error tab
    window.error_text = QTextEdit()
    window.error_text.setReadOnly(True)
    results_tab.addTab(window.error_text, "Errors")
    
    return results_tab