from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from lexer.lexer import Lexer
from parser.parser import Parser
from .components import create_input_section, create_results_section
from .styles import apply_styles
from .tree_visualizer import ParseTreeVisualizer

class SyntaxAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lexer = Lexer()
        self.parser = Parser()
        self.visualizer = ParseTreeVisualizer()
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Advanced Code Analyzer")
        self.setGeometry(100, 100, 1200, 800)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create UI components
        input_frame = create_input_section(self)
        self.results_tab = create_results_section(self)
        
        layout.addWidget(input_frame)
        layout.addWidget(self.results_tab)
        
        apply_styles(self)

    def analyze_code(self):
        """Analyze the input code and display results"""
        code = self.input_text.toPlainText().strip()
        if not code:
            self.show_error_message("Please enter code to analyze.")
            return
            
        self.clear_results()
        
        try:
            # Perform lexical analysis
            tokens = self.lexer.tokenize(code)
            self.update_token_table(tokens)
            
            if self.lexer.errors:
                self.show_errors(self.lexer.errors)
                return
                
            # Perform syntax analysis
            parse_tree = self.parser.parse(tokens)
            
            if self.parser.errors:
                self.show_errors(self.parser.errors)
            elif parse_tree:
                self.display_parse_tree(parse_tree)
                
        except Exception as e:
            self.show_errors([f"Error during analysis: {str(e)}"])
    
    def update_token_table(self, tokens):
        """Update the token analysis table"""
        from PyQt5.QtWidgets import QTableWidgetItem
        self.token_table.setRowCount(len(tokens))
        for i, token in enumerate(tokens):
            self.token_table.setItem(i, 0, QTableWidgetItem(token.type))
            self.token_table.setItem(i, 1, QTableWidgetItem(str(token.value)))
            self.token_table.setItem(i, 2, QTableWidgetItem(str(token.position)))
            self.token_table.setItem(i, 3, QTableWidgetItem(str(token.line)))
        self.token_table.resizeColumnsToContents()
    
    def show_errors(self, errors):
        """Display errors in the error tab"""
        self.error_text.setText("\n".join(errors))
        self.results_tab.setCurrentWidget(self.error_text)
    
    def show_error_message(self, message):
        """Display an error message dialog"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Error", message)
    
    def display_parse_tree(self, parse_tree):
        """Display the parse tree visualization"""
        figure = self.visualizer.visualize(parse_tree)
        if figure:
            canvas = FigureCanvas(figure)
            self.tree_layout.addWidget(canvas)
            self.results_tab.setCurrentWidget(self.tree_widget)
    
    def clear_results(self):
        """Clear all result displays"""
        self.token_table.setRowCount(0)
        self.error_text.clear()
        
        for i in reversed(range(self.tree_layout.count())): 
            widget = self.tree_layout.itemAt(i).widget()
            if isinstance(widget, FigureCanvas):
                plt.close(widget.figure)
            if widget:
                widget.setParent(None)
                widget.deleteLater()
    
    def clear_all(self):
        """Clear all input and results"""
        self.input_text.clear()
        self.clear_results()
        
    def closeEvent(self, event):
        """Handle window close event"""
        self.clear_results()
        super().closeEvent(event)