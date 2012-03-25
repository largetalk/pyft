from ftmsc import core

__all__ = ['IftQISR']

class IftQISR(object):
    def __init__(self, appid = None, timeout = None, vad_enable=0,audio_coding='speex'):
        self.appid = appid
        self.timeout = timeout
        self.vad_enable = vad_enable
        self.audio_coding = audio_coding
        self.init_flag = False

    def init(self):
        if self.appid is None:
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
        




            
