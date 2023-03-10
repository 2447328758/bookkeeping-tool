from br import *
from datetime import date

class Bill:
    def __init__(self,indate,money,way,src,pur,id) -> None:
        self.strdate=str(indate)
        self.way=str(way)
        self.src=str(src)
        self.money=str(money)
        self.id=str(id)
        self.pur=str(pur)
        self.args=[]
        self.initArgs()
    
    def initArgs(self):
        '''初始化参数列表'''
        way = WAY[self.way]
        datetuple=self.strdate.split("/");
        self.args.append(date(int(datetuple[0]),int(datetuple[1]),int(datetuple[2])))
        self.args.append(getTime()[1])
        self.args.append(float(self.money))
        self.args.append(way[0])
        self.args.append(self.src)
        self.args.append(self.pur+(f"({way[1]}{self.id})"))
    
    def save(self):
        '''将账单保存'''
        try:
            modifyDateWithArg(self.strdate,True) 
            insertOne(self.args)
            end()
        except:
            return False
        return True
