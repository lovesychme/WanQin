#_*_ coding:utf-8 _*_
import os.path

import win32com.client
import pythoncom
from xlConst import *
import re
import time

class SWIFT():
    def __init__(self):
        self.closeAllExcel()
        pythoncom.CoInitialize()
        self.excel=win32com.client.DispatchEx('excel.application')
        self.excel.Visible=True
        self.excel.DisplayAlerts=False
        self.wkb=None
        self._errMsg=None
        self._status=''

        self.bankAccountPath=None
        self.sources=None
        self.outDir=None

        self.msgSin=None
    def closeAllExcel(self):
        os.system('taskkill /F /IM excel.exe')
    def readSheet(self,sht):
        maxRow=sht.Cells(sht.Rows.Count,1).End(xlUp).Row
        maxCol=sht.Cells(1,sht.Columns.Count).End(xlToLeft).Column
        headDic={}
        for iCol in range(1,maxCol+1):
            val=sht.Cells(1,iCol).Text
            headDic[iCol]=val

        data=[]
        for iRow in  range(2,maxRow+1):
            dic={}
            for iCol in range(1,maxCol+1):
                head=headDic.get(iCol,None)
                val=sht.Cells(iRow,iCol).Text
                dic[head]=val
            data.append(dic)
        return data

    def readBankAccount(self,bankAccountPath,sheetName='Bank account number'):
        wkb=self.excel.Workbooks.Open(bankAccountPath)
        accSht=None
        for sht in wkb.Sheets:
            if sht.Name== sheetName:
                accSht= sht
                break
        if not accSht:
            self.errMsg=f'未找到{sheetName}工作表'
            return None
        data=self.readSheet(accSht)
        dic={}
        for row in data:
            dic[row['Account Number']]=row

        wkb.Saved=True
        wkb.Close()
        return dic
    def readReport(self,reportPath,sheetName='Report'):
        wkb = self.excel.Workbooks.Open(reportPath,ReadOnly=True)
        sht = None
        for t in wkb.Sheets:
            if t.Name == sheetName:
                sht = t
                break
        if not sht:
            self.errMsg = f'未找到{sheetName}工作表'
            return None

        values=sht.UsedRange.Value
        msgId=None
        item=None
        data={}
        for row in values:
            r0=row[0]
            if r0:
                if re.match(r'Message [0-9]+',r0):
                    msgId=r0
                    item={}
                    continue
                if msgId:
                    if 'Transaction Reference Number' in r0:
                        ls=[x.strip() for x in r0.split('\n')]
                        i=0
                        for s in ls:
                            if 'Account Identification - Account' in s:
                                accountNumber=ls[i+1]
                                item['Account Number']=accountNumber
                                data[accountNumber]=item
                            if 'Closing Balance' in s:
                                dcMark=ls[i+1].replace('DCMark: D/C Mark:','').strip()
                                day=ls[i+2].replace('Date:','').strip()[0:6]
                                currency=ls[i+3].replace('Currency:','').strip()[0:3]
                                balance=ls[i+4].split('#')[1]
                                balance=  '0' if balance in ['0,','0,0','0,00'] else balance
                                item['DCMark']=dcMark
                                item['Date']=day
                                item['Currency']=currency
                                item['Balance']=balance
                            i+=1
        wkb.Saved=True
        wkb.Close()
        return data
    def makeReport(self):
        self.status='Start make swift report'
        self.status='Read bankd account file...'
        accountData=self.readBankAccount(self.bankAccountPath)
        data = []
        data.append(['Account Number', 'Short Name', 'CCY', 'Date', 'Balance', 'DCMark'])
        resultDic={}
        for sourceFile in self.sources:
            self.status = f'Read source file: {sourceFile}'
            reportData=self.readReport(sourceFile)
            self.status=f'Make report:{sourceFile}'

            for account ,accDic in  accountData.items():
                dataExist=False
                item=[None for i in range(7)]
                item[0] = account
                item[1] = accDic['Mapped Short Name']
                item[2] = accDic['CCY']
                if account in reportData:
                    repDic=reportData[account]
                    item[3] = repDic['Date']
                    item[4] = repDic['Balance']
                    item[5] = repDic['DCMark']
                    item[6] = repDic['Currency']
                    dataExist=True

                if account not in resultDic:
                    resultDic[account]=item
                elif dataExist:
                    resultDic[account]=item
        for val in resultDic.values():
            data.append(val)

        wkb=self.excel.Workbooks.Add()
        sht=wkb.Sheets(1)
        sht.Name='Report'
        sht.Cells.NumberFormatLocal = "@"
        for i in range(len(data)):
            sht.Range(sht.Cells(i+1,1),sht.Cells(i+1,6)).Value=data[i]
        for i in range(1,len(data[0])+1):
            sht.Columns(i).EntireColumn.AutoFit()

        self.outDir=self.outDir.strip('\\')

        newPath=f'{self.outDir}\\swift_report_{time.strftime("%Y_%m_%d")}.xlsx'

        if os.path.exists(newPath):
            os.remove(newPath)
        wkb.SaveAs(newPath,xlWorkbookDefault)
        wkb.Close()
        self.status=f'New swfit report: {newPath}'
        return newPath
    def close(self):
        excel=self.excel
        if excel:
            if excel.Workbooks.Count:
                for wkb in excel.Workbooks:
                    wkb.Saved=True
                    wkb.Close()
            excel.Quit()
    @property
    def errMsg(self):
        return self._errMsg
    @errMsg.setter
    def errMsg(self,s):
        if self.msgSin:
            self.msgSin.emit(s)
        self._errMsg=s
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self,s):
        self._status = s
        if self.excel:
            self.excel.StatusBar=s
        if self.msgSin:
            self.msgSin.emit(s)
if __name__=='__main__':
    bankAccountPath = r"C:\Users\p1340814\Desktop\cms\demo\bank account.xlsx"
    reportPath = r"C:\Users\p1340814\Desktop\cms\demo\SWIFT REPORT MT940.xls"
    newPath = r'C:\Users\p1340814\Desktop\cms\demo\SWIFT Report_'+time.strftime("%Y-%m-%d")+'_0936_940.xls'

    swift = SWIFT()
    swift.bankAccountPath=bankAccountPath
    swift.sources=[reportPath]
    swift.outDir=r'C:\Users\p1340814\Desktop\cms\demo'

    newPath=swift.makeReport()
    swift.close()
    print(newPath)