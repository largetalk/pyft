from ftmsc import core

__all__ = ['IftQISR', 'QISRSession']

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
        if self.audio_coding != 'speex-wb':
            init_str += ',coding_libs=%s.so'%self.audio_coding
        else:
            init_str += ',coding_libs=speex.so'

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
            raise QISRSessionParamException
        return QISRSession(kwargs['grammarList'], kwargs['params'], lazy)

class QISRSessionParamException(BaseException): pass

class QISRSession(object):
    def __init__(self, grammarList, params,lazy=False):
        self.sessid = None
        self.grammarList = grammarList
        self.params = params
        if not lazy:
            self.begin()

    def begin(self):
        if self.sessid:
            return
        sessid, err = core.qisrSessionBegin(self.grammarList, self.params)
        if err != 0:
            print 'qisr session begin error, error no is %s'%err
            raise QISRSessionParamException
        self.sessid = sessid
        print 'qisr session begin success'

