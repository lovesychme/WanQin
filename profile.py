#_*_ coding:utf-8 _*_
import configparser
import os

class Profile():
    def __init__(self,path='NCS_AUTO_FROFILE.ini'):
        self.cp=configparser.ConfigParser()
        self.path=path
        self.read(self.path)

    def read(self,path):
        self.cp.read(path)
        self.currentProfile=self.getCurrentProfile()

    def save(self):
        abspath=os.path.abspath(self.path)
        dir=os.path.split(abspath)[0]
        self.mkDir(dir)
        with open(self.path,'w') as f:
            self.cp.write(f)

    def set(self,profile,option,value):
        if profile and  profile not in self.cp.sections():
            self.cp.add_section(profile)
        self.cp.set(profile,option,value)

    def get(self,profile,option,value=None):
        try:
            return self.cp.get(profile,option)
        except:
            if value:
                self.set(profile,option,value)
                return value
            else:
                return None

    def names(self):
        return self.cp.sections()

    def mkDir(self, dir):
        if not os.path.exists(dir):
            supDir=os.path.split(dir)[0]
            if not os.path.exists(supDir):
                self.mkDir(supDir)
            os.mkdir(dir)

    def getCurrentProfile(self):
        for x in self.cp.sections():
            if 'selected' in self.cp[x] and 'current' in self.cp[x]:
                if self.cp[x]['current'].lower()=='true':
                    return x
        sections=self.cp.sections()
        if sections:
            name=self.cp.sections()[0]
        else:
            name=os.environ['USERNAME']
            self.addNewProfile(name)
        self.setCurrentProfile(name)
        return name

    def setCurrentProfile(self, s):
        for x in self.cp.sections():
            self.cp[x]['current'] = 'false'
        for x in self.cp.sections():
            if x==s:
                self.cp[x]['current'] = 'true'
        self.currentProfile=s
    def addNewProfile(self,s):
        self.cp.add_section(s)
    def renameProfile(self,old,new):
        cp=self.cp
        x=cp[old]
        cp.add_section(new)
        for a,b in x.items():
            cp[new][a]=b
        cp.remove_section(old)

    def deleteProfile(self,s):
        self.cp.remove_section(s)

    @property
    def bankAccountPath(self):
        return self.get(self.currentProfile,'Bank Account Path')
    @bankAccountPath.setter
    def bankAccountPath(self,s):
        self.set(self.currentProfile,'Bank Account Path',s)

    @property
    def sourceDir(self):
        return self.get(self.currentProfile, 'Source Directory')
    @sourceDir.setter
    def sourceDir(self, s):
        self.set(self.currentProfile, 'Source Directory', s)

    @property
    def outputDir(self):
        return self.get(self.currentProfile, 'Output Directory')
    @outputDir.setter
    def outputDir(self, s):
        self.set(self.currentProfile, 'Output Directory', s)

    @property
    def selectes(self):
        r=self.get(self.currentProfile, 'Selectes')
        if r:
            return r.split(';')
        else:
            return []
    @selectes.setter
    def selectes(self, s):
        if isinstance(s,(list,tuple)):
            s=';'.join(s)
        self.set(self.currentProfile, 'Selectes', s)

    @property
    def unselectes(self):
        r=self.get(self.currentProfile, 'Unselectes')
        if r:
            return r.split(';')
        else:
            return []
    @unselectes.setter
    def unselectes(self, s):
        if isinstance(s,(list,tuple)):
            s=';'.join(s)
        self.set(self.currentProfile, 'Unselectes', s)

if __name__=='__main__':
    p=Profile()
    p.unselectes=('hello', 'world', 'good')
    print(p.unselectes)
    print(p.getCurrentProfile())
    p.save()
