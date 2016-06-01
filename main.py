try:
    from core import Core
    from gui import Window
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    core=Core()
    gui=Window()
    sys.exit(app.exec_())
except:
    print('Life is BAD :(((')