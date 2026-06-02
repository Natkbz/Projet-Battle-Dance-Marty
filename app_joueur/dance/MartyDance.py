from dance.FileDance import FileDance
from robot.MartyContext import MartyContext
class MartyDance:
    def __init__(self,path,marty_):
        self.marty = marty_
        self.file_dance = FileDance(path)
        self.move = self.file_dance.getMvt()
        self.colorDance = self.file_dance.getColorDance()

