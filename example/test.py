from ftmsc import qisr

appid = "4f68a078"#use yourself appid

def test1():
    conn = qisr.IftQISR(appid)
    conn.init()
    
    sess = conn.createSession(grammarList='', params="ssm=1,sub=iat,auf=audio/L16;rate=16000,aue=speex-wb,ent=sms16k,rst=plain,coding_libs=speex.so")
    #sess = conn.createSession(grammarList='', params="ssm=1,sub=iat,auf=audio/L16;rate=8000,aue=speex,ent=sms8k,rst=plain")
    print sess.sessid
    with open('test.wav', 'rb') as fp:
        sess.uploadAudio(fp)
    print sess.getResult()
    conn.fini()

if __name__ == '__main__':
    test1()

