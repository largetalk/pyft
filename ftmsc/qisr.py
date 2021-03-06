from ftmsc import core
import time
from utils import safe_decode

__all__ = ['IftQISR', 'QISRSession']

audiolib_dic = {'speex': 'libspeex.so', 'speex-wb': 'libspeex.so', 'amr': 'libamr.so', 'amr-wb': 'libamr_wb.so'}

class IftQISR(object):
    def __init__(self, appid = None, timeout = None, vad_enable=0,audio_coding='speex'):
        self.appid = appid
        self.timeout = timeout
        self.vad_enable = vad_enable
        self.audio_coding = audio_coding
        self.init_flag = False

    def init(self):
        if not self.appid:
            print 'appid can\'t be None'
            return
        init_str = 'appid=%s,vad_enable=%s,audio_coding=%s'%(self.appid, self.vad_enable, self.audio_coding)
        if self.timeout:
            init_str += ',%s'%self.timeout
        if self.audio_coding in audiolib_dic:
            init_str += ',coding_libs=%s'%audiolib_dic[self.audio_coding]

        print 'qisr init str is %s'%init_str
        err = core.qisrInit(init_str)
        if err != 0:
            print 'qisr init error, error no is %s'%err
        else:
            self.init_flag = True
        return err

    def createSession(self,lazy=False,*args, **kwargs):
        if not self.init_flag:
            print 'init qisr first'
            return
        if 'grammarList' not in kwargs and 'params' not in kwargs:
            raise QISRSessionParamException("require parameter 'grammarList' and 'params' when you init QISRSession")
        return QISRSession(kwargs['grammarList'], kwargs['params'], lazy)

    def fini(self):
        err = core.qisrFini()
        self.init_flag = False
        if err != 0:
            print 'qisr fini error, error no is %s'%err

class QISRSessionParamException(BaseException): pass

class QISRSession(object):
    def __init__(self, grammarList, params,lazy=False):
        self.sessid = None
        self.grammarList = grammarList
        self.params = params
        self.getResult_flag = False
        if not lazy:
            self.begin()

    def __del__(self):
        if self.sessid:
            err = core.qisrSessionEnd(self.sessid, "normal end")
            if err != 0:
                print "session end error, sessid is %s and error no is %s"%(self.sessid, err)

    def begin(self):
        if self.sessid:
            return
        sessid, err = core.qisrSessionBegin(self.grammarList, self.params)
        if err != 0:
            raise QISRSessionParamException('qisr session begin error, error no is %s'%err)

        self.sessid = sessid
        print 'qisr session begin success'

    def uploadAudio(self, fileObj):
        self.getResult_flag = False
        if not hasattr(fileObj, 'read'):
            raise QISRSessionParamException("uploadAudio function except file like object")
        data = fileObj.read(1024 * 8) 
        while data != '':
            err, ep, recog = core.qisrAudioWrite(self.sessid, data, 2)
            print err, ep, recog
            if err != 0:
                raise QISRSessionParamException('qisr upload audio error, error no is %s'%err)
            if ep >= 3:#epStaus >=3, should cancel upload audio
                print 'epstatus exception when upload audio, epstaus value is', ep 
                break
            time.sleep(0.5)
            data = fileObj.read(1024 * 8)

        err, ep, recog = core.qisrAudioWrite(self.sessid, '', 4)
        if err != 0:
            raise QISRSessionParamException('qisr upload audio error, error no is %s'%err)
        if recog != 1 or recog != 2:
            self.getResult_flag = True
            print 'qisr uploadAudio success with recog is %s'%recog
        else:
            print 'qisr error with unknow error and recog is %s'%recog

    def getResult(self, waitTime=5000):
        if not self.getResult_flag:
            print 'upload audio first'
            return None

        resultData = ''
        while True:
            err, rsltStaus, rsltStr = core.qisrGetResult(self.sessid, waitTime)
            print err, rsltStaus
            if err != 0: # get result err
                print "qisr get result error, error no is %s"%err
                return resultData
            if rsltStaus == 1:
                print 'get result nomatch'
            if rsltStr:
                resultData += rsltStr
            if rsltStaus == 5:
                break
            time.sleep(0.5)

        return safe_decode(resultData)


