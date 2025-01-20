import sys
import os
import matplotlib

# Set backend before importing PyQt
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import QApplication
from gui.main_window import SyntaxAnalyzerGUI

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = SyntaxAnalyzerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()