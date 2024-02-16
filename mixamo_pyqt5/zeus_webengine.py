#pip install PyQt5
#pip install PyQtWebEngine

from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore, QtWebChannel, QtGui
import os

class Link(QtCore.QObject):
    def __init__(self, show, role, log_prefix=['./logs/log',None][0]):
        super().__init__(show)
        self.show = show
        if log_prefix:
            log_name = log_prefix+'_'+role+'.txt'
            os.makedirs(os.path.dirname(log_name), exist_ok=True)
            self.file = open(log_name, 'w+')

    @QtCore.pyqtSlot(str, result=str)
    def call(self, data):
        if hasattr(self, 'file') and self.file:
            self.file.write(data+'\n')
            self.file.flush()

        item = data.split(' $$$ ')
        if item[0] == 'Character':
            self.show.step_character = item[1]
        print('call: '+data)
        return 'call: '+data

class Show(QtWidgets.QMainWindow):
    def __init__(self, app, role):
        super().__init__()
        view = QtWebEngineWidgets.QWebEngineView()
        widget = QtWidgets.QWidget();
        layout = QtWidgets.QVBoxLayout(widget);
        layout.addWidget(view);
        edit = QtWidgets.QLineEdit()
        edit.setValidator(QtGui.QIntValidator())
        layout.addWidget(edit);
        button = QtWidgets.QPushButton("Fire");
        button.setEnabled(False)
        button.clicked.connect(lambda: self.__class__.fire(view, edit, role, self))
        layout.addWidget(button)
        widget.setLayout(layout)
        self.setCentralWidget(widget)       
        #view.page().profile().setCachePath(QtCore.QDir.toNativeSeparators('./mixamo_cache/'))  #QtWebEngineWidgets.QWebEngineProfile.defaultProfile().setCachePath('./mixamo_cache/')
        #view.page().profile().setDownloadPath(QtCore.QDir.toNativeSeparators('./mixamo/'+self.step_character+'/')) 
        view.page().profile().downloadRequested.connect(self.down)
        view.page().setWebChannel(QtWebChannel.QWebChannel(self.centralWidget()))
        view.loadFinished.connect(lambda: self.__class__.gate(view, button) )
        view.setUrl(QtCore.QUrl("https://www.mixamo.com/#/?type=Character&page=1"));
        self.resize(1024,768); self.show();  #self.showMaximized()

    def down(self, item):
        if hasattr(self, 'step_character') and self.step_character:
            item.setDownloadDirectory('../data/mixamo/'+self.step_character.replace('/', '#')+'/')
        item.setDownloadFileName(item.downloadFileName())
        if not os.path.exists(os.path.join(item.downloadDirectory(),item.downloadFileName())):
            item.accept()
            print('down: todo,', item.downloadDirectory()+''+item.downloadFileName(), '$$$')  ##PyQt5.QtWebEngineWidgets.QWebEngineDownloadItem  #C:/4d/mixamo-pyqt5/mixamo_00001  #Ely By K.Atienza.fbx
        else:
            print('down: skip,', item.downloadDirectory()+''+item.downloadFileName(), '***')

    def gate(view, button):
        view.loadFinished.disconnect()
        button.setEnabled(True)

    def fire(view, edit, role, show):
        temp = edit.text()
        if temp and temp!='':
            role = str(temp)
        view.page().webChannel().registerObject("jspy", Link(show, role));
        with open('qwebchannel.js', 'r') as file: view.page().runJavaScript(file.read())
        with open('mixamo.js', 'r') as file: view.page().runJavaScript(file.read()+'\n'+'init('+str(role)+');')

def main(role):
    app = QtWidgets.QApplication([])
    win = Show(app, role)
    app.exec_()

if __name__ == '__main__':
    import sys
    if len(sys.argv)==2:
        main(sys.argv[1])
    else:
        print('python '+sys.argv[0]+' <role(0~108)>')

