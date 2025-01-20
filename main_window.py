from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QTextEdit, QPushButton, QLabel, QFrame, QMessageBox,
                           QTabWidget, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class SyntaxAnalyzerGUI(QMainWindow):
    def clear_results(self):
        """Clear all result displays."""
        self.token_table.setRowCount(0)
        self.error_text.clear()
        
        # Properly clean up matplotlib figures
        for i in reversed(range(self.tree_layout.count())): 
            widget = self.tree_layout.itemAt(i).widget()
            if isinstance(widget, FigureCanvas):
                plt.close(widget.figure)
            if widget:
                widget.setParent(None)
                widget.deleteLater()
    
    def analyze_code(self):
        """Analyze the input code and display results."""
        code = self.input_text.toPlainText().strip()
        if not code:
            QMessageBox.warning(self, "Input Error", "Please enter code to analyze.")
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
                figure = self.visualizer.visualize(parse_tree)
                if figure:
                    canvas = FigureCanvas(figure)
                    self.tree_layout.addWidget(canvas)
                    self.results_tab.setCurrentWidget(self.tree_widget)
        except Exception as e:
            self.show_errors([f"Error during analysis: {str(e)}"])
            
    def closeEvent(self, event):
        """Clean up resources when closing the window."""
        self.clear_results()
        super().closeEvent(event)