from PyQt5 import QtCore, QtGui, QtWidgets
from musicdownload import Ui_MainWindow
import requests
import json
import os

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.songName = ''
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }
        # self.get_mid()
        # self.get_findUrl()
        # self.get_music_url()
        # self.download()
        self.pushButton.clicked.connect(self.check_name)
        self.pushButton_2.clicked.connect(self.choice_music)
        self.pushButton_3.clicked.connect(self.downloadmusic)
        self.pushButton_4.clicked.connect(self.clear_lineEdit)

    def clear_lineEdit(self):
        self.lineEdit_2.setText("")

    def check_name(self):
        self.label_4.setText("未下载")
        self.songName = self.lineEdit.text()
        self.get_mid()

    def choice_music(self):
        choose = int(self.lineEdit_2.text())
        self.label_5.setText("你选择了"+str(choose))
        # 获取歌手名字
        singer = ""
        for each in self.dict_["data"]["song"]["list"][choose]["singer"]:
            singer = singer + each["name"] + "/"
        singer = singer[:-1]

        self.filename = self.dict_["data"]["song"]["list"][choose]["title"] + "-" + singer
        self.songmid = self.dict_["data"]["song"]["list"][choose]["mid"]

    def downloadmusic(self):
        if not os.path.exists("QQmusic"):
            os.mkdir("QQmusic")
        self.get_findUrl()
        self.get_music_url()
        self.download()
        self.label_4.setText("下载完成")
        self.dict_ = {}
        self.textBrowser.setText("")
        self.lineEdit_2.setText("")
        self.label_5.setText("你还没选择")

    def get_mid(self):
        self.textBrowser.setText("")
        url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=62271055844917057&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w="+self.songName+"&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0"
        r = requests.get(url, headers=self.headers)
        self.dict_ = json.loads(r.text)

        # 打印信息
        index = 0
        for eachSong in self.dict_["data"]["song"]["list"]:
            singer = ""
            for eachone in eachSong["singer"]:
                singer = singer + eachone["name"] + "/"
            singer = singer[:-1]
            self.textBrowser.append(str(index) + '   ' + str(eachSong["title"]) + '   ' + str(singer))
            index += 1

    def get_findUrl(self):
        songvkey = "8495737995507689"
        dict_ = {
            "req": {
                "module": "CDN.SrfCdnDispatchServer",
                "method": "GetCdnDispatch",
                "param": {
                    "guid": "4787729008",
                    "calltype": 0,
                    "userip": ""
                }
            },
            "req_0": {
                "module": "vkey.GetVkeyServer",
                "method": "CgiGetVkey",
                "param": {
                    "guid": "4787729008",
                    "songmid": [str(self.songmid)],
                    "songtype": [0],
                    "uin": "0",
                    "loginflag": 1,
                    "platform": "20"
                }
            },
            "comm": {
                "uin": 0,
                "format": "json",
                "ct": 24,
                "cv": 0
            }
        }
        dict_ = json.dumps(dict_)
        self.findUrl = "https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey"+str(songvkey)+"&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data="+dict_

    def get_music_url(self):
        r = requests.get(self.findUrl, headers=self.headers)
        dict_ = json.loads(r.text)
        music_url = dict_["req_0"]["data"]["midurlinfo"][0]["purl"]
        music_url = "http://124.89.197.22/amobile.music.tc.qq.com/" + music_url
        self.music_url = music_url

    def download(self):
        r = requests.get(self.music_url, headers=self.headers)
        name = "QQmusic/" + self.filename + ".mp3"
        with open(name, "wb") as f:
            f.write(r.content)