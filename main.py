import os
import re
import sys
import json
import codecs
<<<<<<< HEAD
=======
import git
>>>>>>> c43a0a84dfc601221094ca24104e39707615ad85
import shutil
import pprint
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import *

class jspaser:
    def __init__(self, config_src):
        self.config = {}
        with open(config_src, "r", encoding="utf-8") as config:
            self.config = json.load(config)

    def open_js(self) -> list:
        result = []
        filedir = os.path.join(self.config["dccon_list_src"], "dccon_list.js")
        with codecs.open(filedir, "r", encoding = "UTF-8-sig") as dccon_list:
            js_data = dccon_list.read()
            matcher = re.compile(r"(.*?)= (\[(.|\s)*\])")

            js_data = matcher.search(js_data).group(2)
            js_data = js_data[1:-1].split("},")

            for data in js_data:
                data = data.strip()
                data = data[-1:]=="}" and data or data +"}"
                try:
                    result.append(json.loads(data))
                except Exception:
                    raise Exception

        return result

    def write_js(self, data: list):
        try:
            valname = self.config["dccon_list_varname"]
            filedir = os.path.join(self.config["dccon_list_src"], "dccon_list.js")

            with codecs.open(filedir, "w+", encoding="UTF-8-sig") as file:
<<<<<<< HEAD
                file.write(" {0} = [\n".format(valname))
=======
                file.write("{0} = [\n".format(valname))
>>>>>>> c43a0a84dfc601221094ca24104e39707615ad85
                for idx, i in enumerate(data):
                    string = json.dumps(i, ensure_ascii=False)
                    if idx < len(data)-1:
                        string += ","
                    string+= "\n"
                    file.write(string)
                
                file.write("];")


        except Exception:
            raise Exception

class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal() # signal when the text entry is left clicked

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: self.clicked.emit()
        else: super().mousePressEvent(event)

class ConfigWindow(QDialog):
    def __init__(self, config_src, config):
        super().__init__()
        self.config_src = config_src
        self.config = config
        self.initUI()

    def initUI(self):
        self.setWindowTitle("디시콘 등록기 설정")
        self.resize(500, 300)
        mainLayout = QVBoxLayout()
        subLayout = QHBoxLayout()

        tagLayout = QVBoxLayout()
        lbl_gitID = QLabel("깃허브 아이디: ", self)
        lbl_repo = QLabel("레포지토리 주소: ", self)
        lbl_list_varname = QLabel("dccon.js 변수이름: ", self)
        lbl_list_src = QLabel("dccon.js 위치: ", self)
        lbl_back_src = QLabel("dccon.js 백업: ", self)
        lbl_image_src = QLabel("디시콘 이미지 위치: ", self)

        tagLayout.addWidget(lbl_gitID)
        tagLayout.addWidget(lbl_repo)
        tagLayout.addWidget(lbl_list_varname)
        tagLayout.addWidget(lbl_list_src)
        tagLayout.addWidget(lbl_back_src)
        tagLayout.addWidget(lbl_image_src)

        subLayout.addLayout(tagLayout)

        lineLayout = QVBoxLayout()
        self.gitID = QLineEdit(self)
        self.gitID.setPlaceholderText("깃허브 아이디를 입력해주세요")
        self.gitID.setText(self.config["git_id"])

        self.repo = QLineEdit(self)
        self.repo.setPlaceholderText("깃허브 레포지토리 url을 입력해주세요.")
        self.repo.setText(self.config["repo"])

        self.dccon_list_varname = QLineEdit(self)
        self.dccon_list_varname.setPlaceholderText("dccon_list.js의 변수이름을 입력해주세요.")
        self.dccon_list_varname.setText(self.config["dccon_list_varname"])

        self.dccon_list_src = ClickableLineEdit(self)
        self.dccon_list_src.setPlaceholderText("dccon_list.js의 위치를 입력해주세요.")
        self.dccon_list_src.setText(self.config["dccon_list_src"])
        self.dccon_list_src.clicked.connect(self.set_dccon_list_src)


        self.dccon_list_backup = ClickableLineEdit(self)
        self.dccon_list_backup.setPlaceholderText("dccon_list.js의 백업 위치를 입력해주세요.")
        self.dccon_list_backup.setText(self.config["dccon_list_backup"])
        self.dccon_list_backup.clicked.connect(self.set_dccon_list_backup)

        self.dccon_image_source = ClickableLineEdit(self)
        self.dccon_image_source.setPlaceholderText("디시콘 이미지를 저장하는 디렉토리 위치를 설정해주세요.")
        self.dccon_image_source.setText(self.config["dccon_image_source"])
        self.dccon_image_source.clicked.connect(self.set_dccon_image_source)
        
        lineLayout.addWidget(self.gitID)
        lineLayout.addWidget(self.repo)
        lineLayout.addWidget(self.dccon_list_varname)
        lineLayout.addWidget(self.dccon_list_src)
        lineLayout.addWidget(self.dccon_list_backup)
        lineLayout.addWidget(self.dccon_image_source)

        subLayout.addLayout(lineLayout)

        mainLayout.addLayout(subLayout)

        btnLayout = QHBoxLayout()
        self.btn_save = QPushButton("설정 저장")
        self.btn_save.clicked.connect(self.on_save)
    
        self.btn_cancel = QPushButton("취소")
        self.btn_cancel.clicked.connect(self.on_cancel)
        btnLayout.addWidget(self.btn_save)
        btnLayout.addWidget(self.btn_cancel)

        mainLayout.addLayout(btnLayout)

        self.setLayout(mainLayout)

    def showModal(self):
        return super().exec_()

    def on_cancel(self):
        self.reject()

    def on_save(self):
        reply = QMessageBox.question(self, "메세지", "설정을 저장하시겠습니까?",
                                            QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            QMessageBox.warning(self, "알림", "설정 저장을 취소하였습니다.")
            return

        result = {
            "git_id": self.gitID.text(),
            "repo": self.repo.text(),
            "dccon_list_varname": self.dccon_list_varname.text(),
            "dccon_list_src": self.dccon_list_src.text(),
            "dccon_list_backup": self.dccon_list_backup.text(),
            "dccon_image_source": self.dccon_image_source.text()
        }
        with open(self.config_src, "w+", encoding="utf-8") as file:
            json.dump(result, file, indent=4)
        QMessageBox.warning(self, "알림", "설정을 저장하였습니다.")
        self.accept()

    def set_dccon_list_src(self):
        fname = QFileDialog.getExistingDirectory(self, "dccon_list.js가 있는 폴더", "./")
        if fname != "":
            relpath = os.path.relpath(fname, (os.path.dirname(os.path.realpath(__file__))))
            self.dccon_list_src.setText(relpath)

    def set_dccon_list_backup(self):
        fname = QFileDialog.getExistingDirectory(self, "dccon_list.js를 백업할 폴더", "./")
        if fname != "":
            relpath = os.path.relpath(fname, (os.path.dirname(os.path.realpath(__file__))))
            self.dccon_list_backup.setText(relpath)

    def set_dccon_image_source(self):
        fname = QFileDialog.getExistingDirectory(self, "디시콘 이미지가 있는 폴더", "./")
        if fname != "":
            relpath = os.path.relpath(fname, (os.path.dirname(os.path.realpath(__file__))))
            self.dccon_image_source.setText(relpath)

class Window(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config_src = config
        self.setAcceptDrops(True)
        self.config = self.setconfig(config)
        self.log = ""
        self.targetsrc = ""
        self.result = []
        self.initUI()
        self.setAcceptDrops(True)

    def setconfig(self, config) -> dict:
        result = {"git_id": "","repo": "", "dccon_list_varname": "",
                    "dccon_list_src": "", "dccon_list_backup": "", "dccon_image_source": ""
        }
        try:
            with open(config, "r", encoding="utf-8") as data:
                result = json.load(data)

        except Exception:
            QMessageBox.warning(self, "경고", "config.json파일을 찾을 수 없어\n새로 생성하였습니다.")
            with open(config, "w+", encoding="utf-8") as file:
                json.dump(result, file, indent=4)

        return result

    def backup(self):
        if self.config["dccon_list_backup"] == "":
            return False

        try:
            dir = self.config["dccon_list_backup"]
            if not os.path.exists(dir):
                os.makedirs(dir)
            
            src = os.path.join(self.config["dccon_list_src"], "dccon_list.js")
            dest = self.config["dccon_list_backup"]
            for i in range(0, 10):
                wdest = os.path.join(dest, "dccon_list{0}.js".format(i))
                if not os.path.exists(wdest):
                    shutil.copyfile(src, wdest)
                    return True

            dest = os.path.join(dest, "dccon_list10.js")
            shutil.copyfile(src, dest)
            return True

        except OSError as e:
            print(e)
            QMessageBox.warning(self, "경고", "백업파일을 생성할 수 없었습니다.\n관리자 권한으로 실행하시거나\nconfig.json의 dccon_list_backup의 설정을 유효한 경로로 변경해주세요.")
            return False

    def initUI(self):
        configAction = QAction("속성", self)
        configAction.setShortcut("Ctrl+P")
        configAction.setStatusTip("프로그램의 속성을 설정합니다.")
        configAction.triggered.connect(self.on_setting)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("파일")
        filemenu.addAction(configAction)

        widget = QWidget()
        mainLayout = QHBoxLayout()

        leftLayout = QVBoxLayout()

        leftupLayout = QGridLayout()
        lbl_img = QLabel("이미지", self)
        leftupLayout.addWidget(lbl_img, 0, 0)

        self.lbl_pixmap = QLabel(self)
        self.lbl_pixmap.setMaximumHeight(600)
        self.lbl_pixmap.setAcceptDrops(True)
        self.pixmap = QPixmap()
        self.lbl_pixmap.setPixmap(self.pixmap)
        leftupLayout.addWidget(self.lbl_pixmap, 0, 1)

        leftdownLayout = QHBoxLayout()

        subleftdownLayout = QHBoxLayout()

        tagLayout = QVBoxLayout()
        lbl_name = QLabel("이름", self)
        tagLayout.addWidget(lbl_name)
        lbl_keywords = QLabel("키워드", self)
        tagLayout.addWidget(lbl_keywords)
        lbl_tags = QLabel("태그", self)
        tagLayout.addWidget(lbl_tags)
        subleftdownLayout.addLayout(tagLayout)

        inputLayout = QVBoxLayout()
        self.let_name = QLineEdit(self)
        self.let_name.setPlaceholderText("이미지를 드래그앤 드롭하면 자동으로 변경됩니다.")
        self.let_name.setReadOnly(True)
        inputLayout.addWidget(self.let_name)
        self.let_keywords = QLineEdit(self)
        self.let_keywords.setPlaceholderText("복수의 키워드는 쉼표로 구분해주세요.")
        inputLayout.addWidget(self.let_keywords)
        self.let_tags = QLineEdit(self)
        self.let_tags.setPlaceholderText("복수의 태그는 쉼표로 구분해주세요.")
        inputLayout.addWidget(self.let_tags)
        subleftdownLayout.addLayout(inputLayout)

        enrollLayout = QVBoxLayout()
        self.btn_enroll = QPushButton("등록", self)
        self.btn_enroll.setMaximumHeight(100)
        self.btn_enroll.setCheckable(True)
        self.btn_enroll.toggle()
        self.btn_enroll.clicked.connect(self.on_enroll)
        enrollLayout.addWidget(self.btn_enroll)
        subleftdownLayout.addLayout(enrollLayout)

        leftdownLayout.addLayout(subleftdownLayout)

        leftLayout.addLayout(leftupLayout)
        leftLayout.addLayout(leftdownLayout)

        rightLayout = QVBoxLayout()

        rightlogLayout = QVBoxLayout()
        lbl_log = QLabel("로그", self)
        self.tet_log = QTextEdit(self)
        self.tet_log.setReadOnly(True)
        rightlogLayout.addWidget(lbl_log)
        rightlogLayout.addWidget(self.tet_log)

        rightLayout.addLayout(rightlogLayout)

        rightcancelLayout = QHBoxLayout()
        lbl_cancel = QLabel("취소할 작업", self)
        self.let_cancel = QLineEdit(self)
        self.let_cancel.setPlaceholderText("취소할 작업의 인덱스를 입력해주세요. (쉼표로 구분)")
        self.btn_cancel = QPushButton("작업취소", self)
        self.btn_cancel.setMaximumHeight(300)
        self.btn_cancel.clicked.connect(self.on_cancel)
        rightcancelLayout.addWidget(lbl_cancel)
        rightcancelLayout.addWidget(self.let_cancel)
        rightcancelLayout.addWidget(self.btn_cancel)

        rightLayout.addLayout(rightcancelLayout)

        self.btn_accept = QPushButton("내보내기", self)
        self.btn_accept.setCheckable(True)
        self.btn_accept.toggle()
        self.btn_accept.clicked.connect(self.on_accept)
        rightLayout.addWidget(self.btn_accept)

        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)

        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        self.setWindowTitle("쪽쪽야옹")
        self.move(300, 300)
        self.resize(1300, 600)
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.targetsrc = [f for f in files][0]
        _, tail = os.path.split(self.targetsrc)
        self.pixmap.load(self.targetsrc)
        self.lbl_pixmap.setPixmap(self.pixmap)
        self.let_name.setText(tail)

    def on_enroll(self):
        if self.targetsrc == "":
            QMessageBox.warning(self, "오류", "이미지를 프로그램에 등록해주세요")
            return

        entitiy = {
            "src": self.targetsrc,
            "name": self.let_name.text(),
            "keywords": [i.strip() for i in self.let_keywords.text().split(",")],
            "tags": [i.strip() for i in self.let_tags.text().split(",")]
        }
        self.result.append(entitiy)
        self.pixmap.load("")
        self.lbl_pixmap.setPixmap(self.pixmap)
        self.targetsrc = ""
        self.let_name.setText("")
        self.let_keywords.setText("")
        self.let_tags.setText("")
        self.tet_log.append("{0}: {1[src]}\n[{1[name]}] keywords: {1[keywords]}, tags: {1[tags]}\n===".format(len(self.result), entitiy))
    
    def on_accept(self):
        reply = QMessageBox.question(self, "메세지", "정말로 내보내기를 진행합니까?",
                                            QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            QMessageBox.warning(self, "알림", "내보내기를 취소하였습니다.")
            return

        self.tet_log.append("내보내기를 시작합니다\n등록한 이미지를 {0}에 이동합니다...\n".format(self.config["dccon_image_source"]))

        total_task = len(self.result)
        current_task = 0
        for idx, data in enumerate(self.result):
            try:
                src =  data["src"]
                dest = self.config["dccon_image_source"]
                print(src, dest)
                print(shutil.copy(src, dest))
                #shutil.copyfile(src, dest)
                current_task += 1
            except Exception as e:
                self.tet_log.append("오류 발생!\n{0}번째 이미지\n{1}\n===\n".format(idx, e))

        self.tet_log.append("[{0}/{1}] 의 작업을 완료하였습니다.\n".format(total_task, current_task))
        self.tet_log.append("dccon_list.js 파일의 재구성을 시작합니다.\n")

        self.tet_log.append("{0}에 백업을 진행중...\n".format(self.config["dccon_list_backup"]))
        flag = self.backup()
        self.tet_log.append("{0}에 백업을 완료!\n".format(self.config["dccon_list_backup"]))

        reply = QMessageBox.Yes
        if flag == False:
            reply = QMessageBox.question(self, "메세지", "dccon_list.js 파일의 백업에 실패하였습니다\n정말로 내보내기를 계속하시겠습니까?",
                                            QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No:
            self.tet_log.append("작업을 취소하였습니다.\n")
            self.tet_log.append("내보내기를 종료합니다.\n")
            return 

        try:
            self.tet_log.append("dccon_list.js를 불러옵니다.\n")
            jsp = jspaser(self.config_src)
            js_data = jsp.open_js()
        
            self.tet_log.append("dccon_list.js를 재구성합니다...\n")
            self.result = [{k: v for k, v in i.items() if k not in ["src", "dest"]}for i in self.result]
            jsp.write_js(js_data + self.result)
            self.result = []
            self.tet_log.append("dccon_list.js를 재구성을 완료하였습니다!\n내보내기를 종료합니다\n")
        
        except Exception as e:
            self.tet_log.append("dccon_list.js 재구성에 실패하였습니다.\n{0}\n===\n".format(e))


    def on_cancel(self):
        reply = QMessageBox.question(self, "메세지", "정말로 선택한 작업을 취소하시겠습니까?",
                                            QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if self.let_cancel.text() == "":
            QMessageBox.warning(self, "경고", "취소할 작업이 없습니다.")
            return

        temp = self.result
        try:
            temp = [item for idx, item in enumerate(temp) if idx not in [int(i.strip())-1 for i in self.let_cancel.text().split(",")]]
            string = ""
            for idx, item in enumerate(temp):
                string += "{0}: {1[src]}\n[{1[name]}] keywords: {1[keywords]}, tags: {1[tags]}\n===\n".format(idx+1, item)
            self.tet_log.setText(string)
            self.let_cancel.setText("")
            self.result = temp

        except Exception:
            QMessageBox.warning(self, "경고", "작업을 정상적으로 취소할 수 없었습니다.\n다시 시도해주세요.")
            return

    def on_setting(self):
        win = ConfigWindow(self.config_src, self.config)
        r = win.showModal()
        if r:
            self.config = self.setconfig(self.config_src)
            
def main():
    app = QApplication(sys.argv)
    window = Window("./config.json")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
