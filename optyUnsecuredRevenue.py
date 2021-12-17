import os,sys
'''
功能描述
遍历数据,取"Proposal No"的值:
1, 'Proposal No'值为:'3-0000074813' 或 "3-0000084422" , 将"Opportunity Currency"改CNY为:RMB
2, 'Proposal No'值为: 
    3-0000080029
    3-0000083470
    3-0000084695
    3-0000084698
    3-0000084963
    3-0000087361
    3-0000091543
    3-0000091544
    它们的"Opportunity Currency"值不为RMB和SGD,将整行数据删除.
3, "Proposal No"值为:"3-0000092798" 或 "3-0000092830" 将"Contracting Customer / Partner" 和 "End Customer" 值改成:"HUAWEI TECHNOLOGIES CO., LTD. (H&T)"
4, 'Proposal No'值为:'3-0000086082'   将"Expected Award Date"改为2021年1月31日，
'''

from excelSht import *
from excelUtil import *

class OUR(ExcelSht):
    def __init__(self):
        super(OUR, self).__init__()
        self.errMsg=None
        self.sources=None
        self.outDir=None
        self.excel=None
        self.msgSin=None
        self.statusList=[]

    def processAll(self) ->list:
        if not self.sources:
            self.errMsg='没有源数据.'
            return None
        outs=[]
        for f in self.sources:
            out=self.process(f)
            outs.append(out)
        self.setLevelStatus("完成")
        self.close()
        return outs
    def process(self,f:str) -> str:
        if not os.path.exists(f):
            self.errMsg=f'文件路径不存在:{f}'
            return None
        if not self.excel:
            self.excel=self.newExcel()
        self.setLevelStatus(f'处理文件:{os.path.split(f)[1]}', 1)

        excel=self.excel
        wkb=self.openWkb(excel,f,readOnly=True)
        names=[x.Name for x in wkb.Sheets]
        shtName='UnsecuredRevenue'
        if shtName not in names:
            self.errMsg=f'文件:{f}中找不到工作薄:{shtName}'
            return None
        sht=wkb.Sheets(shtName)

        self.headRow=3
        self.initExcelSht(sht)

        self.opportunityCurrency()
        self.customerAndDate()

        sourceDir, fileName = os.path.split(f)
        if self.outDir and os.path.exists(self.outDir):
            outDir=self.outDir
        else:
            outDir=sourceDir
        a,b=os.path.splitext(fileName)
        outPath=f'{outDir}\\{a}_Auto{b}'

        if os.path.exists(outPath):
            os.remove(outPath)
        wkb.SaveAs(outPath)
        wkb.Close()
        self.setLevelStatus(f'保存文件:{outPath}',1)
        return outPath
    def opportunityCurrency(self):
        self.setLevelStatus('Opportunity Currency',2)
        sht=self.sht
        excel=sht.Parent.Parent
        proCol=self.getCol("Proposal No")
        optCol=self.getCol('Opportunity Currency')

        cnys=['3-0000074813','3-0000084422']
        dels=['3-0000080029','3-0000083470','3-0000084695','3-0000084698','3-0000084963','3-0000087361','3-0000091543','3-0000091544']
        delRng = None
        for iRow in range(self.maxRow,self.headRow,-1):
            proVal=sht.Cells(iRow,proCol).Value
            if isinstance(proVal,str):
                if proVal in cnys:
                    self.setValueColor(sht.Cells(iRow,optCol),'RMB',0xFF)
                elif proVal in dels:
                    if delRng is None:
                        delRng=sht.Rows(iRow)
                    else:
                        delRng=excel.Union(delRng,sht.Rows(iRow))
        if delRng is not None:
            self.deleteRngXlUp(delRng)
    def customerAndDate(self):
        self.setLevelStatus("Customer和日期",2)
        sht=self.sht
        proCol=self.getCol("Proposal No")
        conCol=self.getCol('Contracting Customer / Partner')
        endCol=self.getCol('End Customer')
        dateCol = self.getCol('Expected Award Date')
        hts=["3-0000092798" ,"3-0000092830"]

        for iRow in range(self.headRow+1,self.maxRow+1):
            proVal=sht.Cells(iRow,proCol).Value
            if proVal in hts:
                self.setValueColor(sht.Cells(iRow, conCol), 'HUAWEI TECHNOLOGIES CO., LTD. (H&T)', 0xff)
                self.setValueColor(sht.Cells(iRow, endCol), 'HUAWEI TECHNOLOGIES CO., LTD. (H&T)', 0xff)
            elif proVal =="3-0000086082":
                self.setValueColor(sht.Cells(iRow,dateCol),'2021/1/31',0xff)

    def setLevelStatus(self,s,level=1):
        l=len(self.statusList)
        if level<=0:
            return
        if level>l:
            self.statusList.append(s)
        elif level<=l:
            self.statusList=self.statusList[0:level]
            self.statusList[-1]=s
        msg=' -->'.join(self.statusList)
        self.setStatus(msg)

    def setStatus(self,s):
        if self.excel:
            self.excel.StatusBar=s
        if self.msgSin:
            self.msgSin.emit(s)
    def close(self):
        if self.excel:
            self.excel.Quit()
if __name__=="__main__":
    f=r"C:\Users\p1340814\Desktop\Wang Qin\OptyUnsecuredRevenue_20211214103752.xlsx"

    o=OUR()
    o.closeAllExcel()
    o.process(f)

    print(o.errMsg)
    print('Done')

