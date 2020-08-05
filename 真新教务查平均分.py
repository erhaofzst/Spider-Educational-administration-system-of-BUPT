js_code = """
		var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

	function encodeInp(input) {
		var output = "";
		var chr1, chr2, chr3 = "";
		var enc1, enc2, enc3, enc4 = "";
		var i = 0;
		do {
			chr1 = input.charCodeAt(i++);
			chr2 = input.charCodeAt(i++);
			chr3 = input.charCodeAt(i++);
			enc1 = chr1 >> 2;
			enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
			enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
			enc4 = chr3 & 63;
			if (isNaN(chr2)) {
				enc3 = enc4 = 64
			} else if (isNaN(chr3)) {
				enc4 = 64
			}
			output = output + keyStr.charAt(enc1) + keyStr.charAt(enc2) + keyStr.charAt(enc3) + keyStr.charAt(enc4);
			chr1 = chr2 = chr3 = "";
			enc1 = enc2 = enc3 = enc4 = ""
		} while (i < input.length);
		return output
	}
		"""
from bs4 import BeautifulSoup
import requests
import execjs
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction,QLabel,QLineEdit,QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets



def web_BUPT(user_name,pass_word):	
	username = user_name
	password = pass_word

	ctx = execjs.compile(js_code)

	account = ctx.call("encodeInp",username)
	passwd = ctx.call("encodeInp",password)
	encoded = account + r"%%%" + passwd

	s = requests.Session()

	url = 'http://jwgl.bupt.edu.cn/jsxsd/xk/LoginToXk'

	r = s.get(url)

	info = {
		'userAccount': username,
		'userPassword': '',
		'encoded': encoded,
	}
	r_in = s.post(url,info)
	#print(r_in.text)
	data = s.get("http://jwgl.bupt.edu.cn/jsxsd/kscj/cjcx_list")
	soup = BeautifulSoup(data.text,'lxml')

	data_list= soup.find_all('tr')
	data_list.pop(0)
	score_all = 0
	credit_all = 0
	for list_all in data_list:
		#print(list_all.find_all("td").text[1])

		score = list_all.text.split()[4]
		credit = list_all.text.split()[5]
		course_type = list_all.text.split()[10]

		if course_type == '任选':
			continue

		if score == '优':
			score = '90'
		if score == '良':
			score = '85'
		if  score == '合格':
			score = '75'
		
		if credit == '免修（不参与计算）':
			continue
		
		score_all = score_all + float(score)*float(credit)
		credit_all = credit_all + float(credit)
	
	x = score_all/credit_all
	return x


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("BUPT_lzt")
        MainWindow.resize(344, 387)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 125, 201, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 0, 211, 81))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 75, 201, 30))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 180, 231, 21))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 220, 151, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 130, 72, 15))
        self.label_5.setObjectName("label_5")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 280, 281, 60))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 344, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.buttonClicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BUPT_lzt"))
        self.label_2.setText(_translate("MainWindow", "学号："))
        self.label_3.setText(_translate("MainWindow", "请输入学号与新教务系统密码"))
        self.label_4.setText(_translate("MainWindow", "（请放心输入，不会有任何泄漏）"))
        self.pushButton.setText(_translate("MainWindow", "看看你的加权平均分"))
        self.label_5.setText(_translate("MainWindow", "密码："))
 
    def buttonClicked(self):
        try:
            b = str(web_BUPT(self.lineEdit.text(),self.lineEdit_2.text()))
            a = "您的学科加权平均分为：" + b
        except Exception:
            a = "学号密码可能出错，如果确认是正确的，请联系QQ:3232752268"   
        
            
        self.textBrowser.setText(a)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = QMainWindow()
    gui_ui = Ui_MainWindow()
    gui_ui.setupUi(gui)

    gui.show()
    sys.exit(app.exec_())
