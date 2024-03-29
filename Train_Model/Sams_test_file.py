import sys
from train_model_container import TrainModelContainer
from new_train_ui import UITrain
from PyQt5.QtWidgets import QApplication
import threading


def launchUI():
    app = QApplication(sys.argv)
    UIWindow = UITrain()
    app.exec()


def main():
    container = TrainModelContainer()
    thread = threading.Thread(target=launchUI)
    thread.start()
    print("hello")
    container.add_train()
    print("Train added")
    print(container.train_list.keys())


if __name__ == "__main__":
    main()
