import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QGridLayout, QFileDialog, QInputDialog, QStyle, QSlider, QDialog, QVBoxLayout, QCheckBox
from PyQt6.QtCore import QDir, QFileInfo
from PyQt6.QtGui import QFont
import sounds
import os


# File Icon: SP_DirIcon
# Name Icon: SP_DialogResetButton

app = QApplication([])

window = QWidget()
window.setWindowTitle("Soundboard")
window.setGeometry(0, 0, 1000, 1000)

DIRECTORY = "/Sounds"

BUTTON_SIZE = 200
SIZE = 5

class Sound(QPushButton):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedSize(BUTTON_SIZE,BUTTON_SIZE)
        self.setFont(QFont("Noto Sans", 20))

        # Button for selecting MP3 File
        self.other_button = QPushButton(self)
        self.other_button.clicked.connect(self.onFileClick)
        self.other_button.setFixedSize(30, 30)
        # Adding the icon for the button
        file_pixmap = QStyle.StandardPixmap.SP_DirIcon
        file_icon = self.style().standardIcon(file_pixmap)
        self.other_button.setIcon(file_icon)
        self.other_button.move(BUTTON_SIZE - self.other_button.size().width() - 5, BUTTON_SIZE - self.other_button.size().height() - 5)

        # Icon for changing name of sound
        self.name_button = QPushButton(self)
        self.clicked.connect(self.onClick)
        # Adding icon for the button
        name_pixmap = QStyle.StandardPixmap.SP_DialogResetButton
        name_icon = self.style().standardIcon(name_pixmap)
        self.name_button.setIcon(name_icon)
        self.name_button.move(5, 5)
        self.name_button.hide()

        # Slider for setting volume
        self.volume_slider = QSlider(self)
        self.volume_slider.move(0, 100)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(200)
        self.volume_slider.setTickInterval(1)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.updateVolume)
        self.volume_slider.hide()

        self.reverse_check_box = QCheckBox(self)
        self.reverse_check_box.setFixedSize(30,30)
        self.reverse_check_box.move(BUTTON_SIZE - self.reverse_check_box.size().width(), 5)
        self.reverse_check_box.stateChanged.connect(self.onReverseClick)
        self.reverse_check_box.hide()
        # print(self.reverse_check_box.size())

        # Gives initial name as empty
        self.name = "Empty"
        self.setText(self.name)
        self.name_button.clicked.connect(self.onNameClick)
        self.id = id
        self.updateData()

    # Updates the data of the sound with the data from the UI
    def updateData(self):
        if soundboard.sounds[self.id] != None:
            self.name = soundboard.sounds[self.id].name
            self.setText(self.name)
            self.volume_slider.setValue(soundboard.sounds[self.id].volume)
            self.volume_slider.show()
            self.name_button.show()
            self.reverse_check_box.show()
            self.reverse_check_box.setChecked(soundboard.sounds[self.id].reversed)
                                        

    def onClick(self):
          if soundboard.sounds[self.id] != None:
            soundboard.sounds[self.id].play()

    # 
    def onFileClick(self):
        file_name, filter = QFileDialog.getOpenFileName(self, "Select a Sound", dir_path + DIRECTORY, "Audio, (*.mp3)")
        path = dir.relativeFilePath(file_name)
        name = QFileInfo(file_name).fileName()
        soundboard.addSound(self.id, path, name, 1, False)
        self.updateData()
        soundboard.saveChanges()
        
    def onNameClick(self):
        text, ok = QInputDialog.getText(self, "Name Dialog", "Enter Name")
        if ok and text != None and text != "":
            self.name = text
            soundboard.sounds[self.id].name = text
            self.updateData()
            soundboard.saveChanges()

    def onReverseClick(self):
        soundboard.sounds[self.id].reversed = self.reverse_check_box.isChecked()
        soundboard.sounds[self.id].makeChanges()
        soundboard.saveChanges()

    def updateVolume(self):
        soundboard.sounds[self.id].volume = (self.volume_slider.value())
        soundboard.sounds[self.id].makeChanges()
        soundboard.saveChanges()


class SettingDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.volume_slider = QSlider()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.volume_slider)

        self.ok_button = QPushButton()
    
    def hideDialog():
        pass

# Gets directory of current script
dir_path = os.getcwd()
dir = QDir(dir_path)
print(dir)


soundboard = sounds.Soundboard()
soundboard.loadChanges()

layout = QGridLayout()


for i in range(SIZE):
    for j in range (SIZE):
        layout.addWidget(Sound(j + (i*5), "Button"), i, j)


window.setLayout(layout)
window.show()
sys.exit(app.exec())