import logging
import os
import time

cd=os.getcwd()
ct=time.strftime("%Y-%m-%d %H-%M",time.localtime(time.time()))
name="%s log.txt" %ct
path=os.path.join(os.getcwd(),"logs",name)
filehandler=logging.FileHandler(path,"w")
format = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
filehandler.setFormatter(format)

def logger(level=logging.DEBUG):
    logger=logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(filehandler)
    return logger


if __name__=="__main__":

    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(filehandler)
    logger.debug("test logging.")