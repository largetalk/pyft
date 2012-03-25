from ftmsc import qisr

appid = ""#use yourself appid

def test1():
    conn = qisr.IftQISR(appid)
    conn.init()
    sess = conn.createSession(grammarList='', params="ssm=1,sub=iat,auf=audio/L16;rate=8000,aue=speex,ent=sms8k,rst=plain")
    print sess.sessid

if __name__ == '__main__':
    test1()

