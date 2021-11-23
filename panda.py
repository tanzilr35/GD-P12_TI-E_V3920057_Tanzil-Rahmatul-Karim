# Line 2-9 = Import data yg diperlukan
from math import pi, sin, cos #untuk memuat library math dengan menginisialisasi variabel pi, sin, dan cos
from random import SystemRandom
from direct.showbase.ShowBase import ShowBase #untuk memuat sebagian besar modul panda3d dan menyebabkan window 3D muncul
from direct.task import Task #untuk memuat manajemen task dengan diinisialisasi menjadi Task
from direct.actor.Actor import Actor #untuk memuat kelas aktor yang berisi metode untuk membuat, memanipulasi, dan memainkan animasi karakter 3D
from direct.interval.IntervalGlobal import Sequence #untuk mengontrol interval 
from panda3d.core import Point3 #untuk mengatur koordinat aktor
from panda3d.core import ClockObject
from panda3d.core import load_prc_file #untuk memuat file prc

# Line 12 = Memanggil file myconfig.prc yg isinya konfigurasi dasar window, seperti title window dan ukurannya
load_prc_file('myconfig.prc') #agar mempersingkat script coding

# Line 15-20 = List map untuk kunci pada keyboard, isinya false secara default
keyMap = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "rotate": False
}

# Line 24-25 = Pembuatan fungsi updateKeyMap dgn memanggil list map kunci untuk bisa diupdate
def updateKeyMap(key, state):
    keyMap[key] = state

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)  #menginisialisasi modul ShowBase

        # Line 32 = Menonaktifkan fungsi mouse sebagai penggerak kamera
        self.disableMouse()

        # Line 35 = Mengload model environtment
        self.scene = self.loader.loadModel("models/environment")
        # Line 37 = Atur ulang model environtmentyang akan dirender
        self.scene.reparentTo(self.render)
        # Line 39-40 = Transformasi skala dan posisi model environtment
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Line 43 = Tambahkan prosedur spinCameraTask ke taskMgr/task manager
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Line 46-48 = Mengload dan mengatur skala aktor panda
        self.Panda = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.Panda.setScale(0.005, 0.005, 0.005)
        self.Panda.reparentTo(self.render) #atur ulang model yang akan dirender
        # Line 51 = Loop animasinya agar bisa bergerak
        self.Panda.loop("walk")

        # Line 54-67 = Membuat aturan key untuk penggunaan keyboard dalam mengarahkan aktor
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])

        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])

        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])

        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])

        self.accept("space", updateKeyMap, ["rotate", True])
        self.accept("space-up", updateKeyMap, ["rotate", False])

        # Line 70-71 = Memberi nilai kecepatan dan angle
        self.speed=6
        self.angle=0  #nilai defaultnya 0

        # Line 74 = Penambahan untuk taskMgr agar program dapat di update
        self.taskMgr.add(self.update, "update")
        self.accept("escape", SystemRandom.exit,[0])
        self.accept("mouse1", self.setMouseBtn, [0,1])
        self.accept("mouse1-up", self.setMouseBtn, [0,0])
        self.accept("mouse2", self.setMouseBtn, [1,1])
        self.accept("mouse2-up", self.setMouseBtn, [1,0])
        self.accept("mouse3", self.setMouseBtn, [2,1])
        self.accept("mouse3-up", self.setMouseBtn, [2,0])
        self.accept("enter", self.toggleShader)
        self.accept("j", self.rotateLight, [-1])
        self.accept("k", self.rotateLight, [1])
        self.accept("arrow_left", self.rotateCam, [-1])
        self.accept("arrow_right", self.rotateCam, [1])

    # Line 77-82 = Pembuatan fungsi spinCamera untuk pemutaran angle dari kamera
    def spinCameraTask(self, task):
        angleDegrees=task.time * 6.0
        angleRadians=angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3) #posisi awal pergerakkan
        self.camera.setHpr(angleDegrees, 0, 0) #mengembalikan kamera ke posisi awal
        return Task.cont

    def update(self, task):

        globalClock = ClockObject.getGlobalClock()

        dt = globalClock.getDt()

        pos = self.Panda.getPos()

        # Line 93-105 = Pengaturan posisi, kecepatan & waktu, dan angle pada kunci keyboard untuk menggerakan aktor
        if keyMap["left"]:
            pos.x -= self.speed * dt
        if keyMap["right"]:
            pos.x += self.speed * dt
        if keyMap["up"]:
            pos.z += self.speed * dt
        if keyMap["down"]:
            pos.z -= self.speed * dt
        if keyMap["rotate"]:
            self.angle += 1
            self.Panda.setH(self.angle)

        self.Panda.setPos(pos)

    def controlCameras(self, task):
        

        return Task.cont


app = MyApp() #inisialisasi class MyApp untuk dijalankan aplikasinya

# Line 113-116 = Pengaturan suara
mySound = app.loader.loadSfx("game-music.ogg") #memanggil musik yang digunakan
mySound.play() #musik dimulai
mySound.setLoop(True) #loop musik
mySound.setVolume(10) #atur suara menjadi 10

app.run() #main loop untuk menjalankan frame window
