
import socket
def varint(x):
    a=[]
    x=x&(2147483648*2-1)
    while x:
        a.append(x&0b01111111|0b10000000)
        x=x>>7
    a=a or [0b10000000]
    a[-1]=a[-1]-0b10000000
    return bytes(a)
def packet(id,data):
    id=varint(id)+bytes(data)

    l=varint(len(id))
    return l+id
def String(s):
    s=s.encode("utf-8")
    return varint(len(s))+s
def unss(x):
    return bytes(divmod(x,256))

def stripuntilzero(x):
    while (1):
        (a,*x)=x
        if not a>>7:
            break
    return bytes(x)

def gett(x):
	if isinstance(x,dict):
		return x.get("text","")+gett(x.get("extra",""))
	if isinstance(x,list):
		return "".join([gett(i) for i in x])
	if isinstance(x,str):
		return x
                


import json
def get (IP,port=25565):
    
    out=(
    packet(0,
    varint(404)+String(IP)+unss(port)+varint(1)
           )
        )

    try:
        s = socket.socket()
        #s.settimeout(2)
        s.connect((IP, port))
        s.send(out)
        s.send(packet(0,b""))
        


        _in=b""
        while 1:
            d = s.recv(1)
            _in+=d
            if not d[0]>>7:
                break
        d=s.recv(sum((j&0b1111111)<<(7*i) for i,j in enumerate(_in)))
        del _in
        

        #print(d)



        
        temp=d

        d=stripuntilzero(d)
        d=stripuntilzero(d)
        d=d.decode("utf-8")
        try:
            parsed = json.loads(d)
            if "favicon" in parsed:
                del parsed["favicon"]
                return json.dumps(parsed, indent=1,ensure_ascii=False)+"\nfavicon已经省略"
            return json.dumps(parsed, indent=1,ensure_ascii=False)
        except Exception:
            return d
                    
    except  Exception as e:
        return "似乎有什么不对:"+str(e)+(str(temp) if "temp" in locals() else ".")
    finally:
        s.close()
        print("###connection closed")


print(get("[[IP]]"))


