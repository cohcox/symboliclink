""" 
FUZE BUILD SELECTOR for use with Dauntless Fuze
Bug where after creation of link, the warning of the path existing does not show up in you select same folder again
Attempted code clean up by creating methods for each MessageBox. This created an issue where the "would you like to overwrite?" box pops up twice. Must investigate further
"""
##To Create .exe
#       1.from the terminal cd into the same directory this script is in
#       2.then type pyinstaller --onefile --windowed --icon=run.ico FuzeBuildSelector.py

import sys, ctypes, os, errno

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLineEdit,
    QMessageBox,
)

# Check if admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
                
        # Window Title and Icon
        self.setWindowTitle("Fuze Build Selector")
        self.setFixedSize(QSize(400, 80))        
        self.setIcon()
                
        # Basic Page Layout
        pagelayout = QVBoxLayout()
        hLayout0 = QHBoxLayout()
        hLayout1 = QHBoxLayout()
        hLayout2 = QHBoxLayout()
        self.stacklayout = QStackedLayout()        
        pagelayout.addLayout(hLayout0)
        pagelayout.addLayout(hLayout1)
        pagelayout.addLayout(hLayout2)
        pagelayout.addLayout(self.stacklayout)
            
        # Hard-coded destination path for link, MUST ALTER FOR SPECIFC SYSTEM
        #This is the REAL path!!!! Uncomment this when moved to the release volume! Will also need to be changed under run_symlink method!!! Line 162
        #dst = "C:/Users/Mri/Desktop/FUZE_Builds_2019.2_StagingParent/fuze"
        dst = "C:/Users/Cody/Desktop/fuze_staging_parent/fuze"
            
        # Horizontal Box Layout 0 (Text Label)
        label = QLabel("Select A Build")
        hLayout0.addWidget(label)
            
        # Horizontal Box Layout 1 (Text Box and Folder Browser)
        self.lineInput = QLineEdit(self)
            
        # If there is a link already established, display link path in text box
        if os.path.isdir(dst):
            self.lineInput.setText(os.readlink(dst))
                        
        hLayout1.addWidget(self.lineInput) # "..." Button          
        btn = QPushButton("...")
        btn.pressed.connect(self.browse_folder)
        hLayout1.addWidget(btn)
                
        # Horizontal Box Layout 2 (Cancel or Save)  
        hLayout2.addStretch()
                
        btn = QPushButton("Cancel")
        btn.pressed.connect(self.on_cancel_clicked)
        hLayout2.addWidget(btn)
                
        btn = QPushButton("Save")
        btn.pressed.connect(self.on_savebtn_clicked)
        hLayout2.addWidget(btn)
                
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
    
    # Message Box methods
    def SelectBuildPath(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon('runningman.png'))
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("ERROR")
        msgBox.setText("Please select a build path")
        msgBox.exec_() 
                
    # Buttons
    # Browse Folder, AKA "..." button
    def browse_folder(self):
        self.stacklayout.setCurrentIndex(2)
        fname = QFileDialog.getExistingDirectory(self)
            
        # Displays selected folder from browse into text box  
        if fname:
            self.lineInput.setText(fname)
                
    # Save button     
    def on_savebtn_clicked(self):
        self.stacklayout.setCurrentIndex(0)
        
        # Message Box methods
        def SelectBuildPath(self):
            msgBox = QMessageBox()
            msgBox.setWindowIcon(QIcon('runningman.png'))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("ERROR")
            msgBox.setText("Please select a build path")
            msgBox.exec_()
        def NotVaildPath(self):
            msgBox = QMessageBox()
            msgBox.setWindowIcon(QIcon('runningman.png'))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("ERROR")
            msgBox.setText("This is not a vaild path")
            msgBox.exec_()
        def SuccessfulBuild(self):
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Success")
            msgBox.setWindowIcon(QIcon('runningman.png'))
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Successfull Build Link")
            msgBox.setText("Link successfull")
            msgBox.exec_()
        def CurrentPath(self):
            msgBox = QMessageBox()
            msgBox.setWindowIcon(QIcon('runningman.png'))
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Current Path")
            msgBox.setText("This is the current path")
            msgBox.exec_()          
    
        # Check if text box has a path 
        if str(self.lineInput.text()) == "":
            
            #SelectBuildPath(self)
            MainWindow.SelectBuildPath(self)
            
        # Check if text input is a valid path
        elif not os.path.exists(str(self.lineInput.text())):
            NotVaildPath(self)
            
        elif str(self.lineInput.text()) != "":                   
            
            # Run the symbolic link creation code
            def run_symlink():
                
                #dst = "C:/Users/Mri/Desktop/FUZE_Builds_2019.2_StagingParent/fuze"
                dst = "C:/Users/Cody/Desktop/fuze_staging_parent/fuze"             
                
                def force_symlink(src, dst):
                    try:
                        # Linking source to destination
                        os.symlink(src, dst)
                                        
                        # Message box to signify successful link creation
                        SuccessfulBuild(self)
                                                    
                    except OSError as e:
                        if os.path.exists(dst):
                            
                            # MessageBox Methods
                            def OverWriteSuccess(self):
                                msgBox = QMessageBox()
                                msgBox.setWindowTitle("Success")
                                msgBox.setWindowIcon(QIcon('runningman.png'))
                                msgBox.setIcon(QMessageBox.Information)
                                msgBox.setText("Successfully Overwritten!")
                                msgBox.exec_()
                            def NeverReachError(self):
                                msgBox = QMessageBox()
                                msgBox.setWindowTitle("Problem")
                                msgBox.setWindowIcon(QIcon('runningman.png'))
                                msgBox.setIcon(QMessageBox.Critical)
                                msgBox.setText("There is an issue, contact the software team")
                                msgBox.exec_()                           
                            def PathOverwrite(self):
                                msgBox = QMessageBox()
                                msgBox.setWindowIcon(QIcon('runningman.png'))
                                msgBox.setIcon(QMessageBox.Question)
                                msgBox.setWindowTitle("Build Overwrite")
                                msgBox.setText("This will alter the main build for Fuze")
                                msgBox.setInformativeText("Would you like the overwrite it?")
                                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                                msgBox.setDefaultButton(QMessageBox.Yes)
                                msgBox.exec_()
                                                        
                                ret = msgBox.exec_()

                                # Successful link creation                        
                                if ret == QMessageBox.Yes:
                                    os.remove(dst)
                                    os.symlink(src, dst)
                                    OverWriteSuccess(self)                       
                                                                                        
                                elif ret == QMessageBox.No:
                                    return
                                                                            
                                # If an error gets to this point, review the code because it should never reach this check
                                else:
                                    NeverReachError(self)
                            
                            # Check if text box has a path 
                            if str(self.lineInput.text()) == "":
                                SelectBuildPath(self)
                
                            # Check if text input is a valid path
                            elif not os.path.exists(str(self.lineInput.text())):
                                NotVaildPath(self)
                                          
                            if str(self.lineInput.text()) != str(os.readlink(dst)):
                                if str(self.lineInput.text()) == str(os.readlink(dst)):
                                    CurrentPath(self)
                                        
                                elif str(self.lineInput.text()) != str(os.readlink(dst)):
                                    PathOverwrite(self)
                            
                            elif str(self.lineInput.text()) == str(os.readlink(dst)):
                                CurrentPath(self)                                     
                src = str(self.lineInput.text())
                force_symlink(src, dst)       
            run_symlink()
                 
    # Cancels the operation            
    def on_cancel_clicked(self):
        self.stacklayout.setCurrentIndex(3)
        sys.exit(0)
            
    # Running Man Icon
    def setIcon(self):
        appIcon = QIcon("runningman.png")
        self.setWindowIcon(appIcon)       

# Main
if __name__=='__main__': 
    if not is_admin():  
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
             
    else:
        app = QApplication(sys.argv)         
        window = MainWindow()
        window.show()
        app.exec_()