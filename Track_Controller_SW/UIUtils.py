import functools

from PyQt5.QtWidgets import QPushButton


def better_button_ret(size=None, text1=None, text2=None, checkable=True, style1=None, style2=None):
    if text1 and not text2:
        text2 = text1
    button = QPushButton()
    button.setCheckable(checkable)
    button.setFixedHeight(24)
    # button.clicked.connect( functools.partial(button_click1, but=button) )
    if checkable:
        # button.setStyleSheet(
        #     "background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
        if text1:
            button.setText(text1)
        else:
            button.setText("Off")
        button.clicked.connect(
            functools.partial(gen_but_tog, but=button, text1=text1, text2=text2, style_on=style1, style_off=style2))
    else:
        # button.setStyleSheet("background-color: rgb(222, 62, 38); border: 2px solid rgb(222, 0, 0); border-radius: 4px")
        if text1:
            button.setText(text2)
    if size:
        button.setFixedWidth(size)
    return button


def gen_but_tog(but, text1=None, text2=None, style_on=None, style_off=None):
    if but.isChecked():
        # but.setStyleSheet(
        #     f"{style_on if style_on else 'background-color: rgb(143, 186, 255); border: 2px solid rgb( 42,  97, 184); border-radius: 6px'}")
        if text1:
            but.setText(text2)
        else:
            but.setText("On")
    else:
        # but.setStyleSheet(
        #     f"{style_off if style_off else 'background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px'}")
        if text1:
            but.setText(text1)
        else:
            but.setText("Off")
