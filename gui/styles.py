def apply_styles(window):
    """Apply styles to GUI components"""
    # Input styling
    window.input_text.setStyleSheet("""
        QTextEdit {
            background-color: #2c3e50;
            color: #ecf0f1;
            border: 2px solid #3498db;
            border-radius: 5px;
            padding: 10px;
            font-family: 'Consolas', monospace;
            font-size: 14px;
        }
    """)
    
    # Button styling
    button_style = """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            font-weight: bold;
            min-width: 120px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #2472a4;
        }
    """
    window.analyze_btn.setStyleSheet(button_style)
    window.clear_btn.setStyleSheet(button_style)
    window.exit_btn.setStyleSheet(button_style)
    
    # Table styling
    window.token_table.setStyleSheet("""
        QTableWidget {
            background-color: #2c3e50;
            color: #ecf0f1;
            gridline-color: #34495e;
            border: none;
        }
        QHeaderView::section {
            background-color: #34495e;
            color: white;
            padding: 8px;
            border: 1px solid #2c3e50;
            font-weight: bold;
        }
        QTableWidget::item {
            padding: 8px;
        }
    """)
    
    # Error text styling
    window.error_text.setStyleSheet("""
        QTextEdit {
            background-color: #2c3e50;
            color: #e74c3c;
            border: none;
            font-family: 'Consolas', monospace;
            font-size: 14px;
            padding: 10px;
        }
    """)