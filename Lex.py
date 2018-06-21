import re

class Lex:

    def __init__(self):
        self.keywords = []
        self.symbols = []
        self.numbers = ['0','1','2','3','4','5','6','7','8','9']
        self.special = ['n','t','a','b','f','r','v','\\',"'",'"','0']
        #self.names = {}
        self.get_words_symbols('symbols' ,self.symbols)
        self.get_words_symbols('keywords' ,self.keywords)

    def get_words_symbols(self,url,ls):
        with open(url,'r') as f:
            if url == 'symbols' :
                string = f.readline()
                strings = string.split()
                for singleS in strings :
                    ls.append(singleS)
                return

            raw_string = f.readline()
            raw_string = raw_string.replace('"','')
            string = raw_string.replace('\n','')
            strings = string.split(',')
            for singleW in strings :
                ls.append(singleW)

    def deltetNote(self,string):#delete note
        pattern_a = r'//.*\n'
        subString = re.sub(pattern_a,'/*',string)
        pattern_b = r'/\*.*\*/'
        p = re.compile(pattern_b,re.S)
        subString = re.sub(p,'/*',subString)
        return subString

    def coding(self):
        i = 0
        self.bianma = {}
        for symbol in self.symbols:
            self.bianma[symbol] = i
            i += 1
        for keyword in self.keywords:
            self.bianma[keyword] = i
            i += 1

    def DFA(self,string,result):
        self.coding()
        state = 'state0'
        tmp = ''

        while len(string)>0 :
            if string[0] == ' ' or string[0] == '\n' or string[0] == '\t':
                if state == 'state0':
                    string = string[1:]

                elif state == 'symbol':
                    result.append((tmp, self.bianma[tmp]))
                    tmp = ''
                    state = 'state0'
                    string = string[1:]

                elif state == 'sharp':
                    if string[0] == ' ':
                        tmp += string[0]
                        string = string[1:]
                    elif string[0] == '/n':
                        result.append((tmp,state))
                        string = string[1:]
                        state = 'state0'
                        tmp = ''
                    else:
                        print('sharp error')
                        break

                elif state == 'Char':
                    if string[0] == ' ':
                        tmp += string[0]
                        string = string[1:]
                    else:
                        print('illegal char') #判断出错
                        break

                elif state == 'String':
                    if string[0] == ' ':
                        tmp += string[0]
                        string = string[1:]
                    else:
                        print('String error')
                        break

                elif state == 'f_d':
                    result.append((int(tmp),82))#int编码82
                    string = string[1:0]
                    tmp = ''
                    state = 'state0'

                elif state == 'float':
                    result.append((float(tmp),83))#float编码83
                    string = string[1:0]
                    tmp = ''
                    state = 'state0'

                elif state == 'v_k':
                    if tmp.lower() in self.keywords:
                        result.append((tmp,self.bianma[tmp.lower()])) #设置大小写不敏感
                    else:
                        '''n = name(tmp)
                        self.name[tmp] = n'''
                        result.append((tmp,84))
                    state = 'state0'
                    tmp = ''

            else:
                if state == 'state0':
                    if string[0] in self.symbols:
                        state = 'symbol'
                        tmp += string[0]
                        string = string[1:]
                    elif string[0] == '#':
                        state = 'sharp'
                        string = string[1:]
                    elif string[0] == "'":
                        state = 'Char'
                        string = string[1:]
                    elif string[0] == '"':
                        state = 'String'
                        string = string[1:]
                    elif string[0] in self.numbers:
                        tmp += string[0]
                        string = string[1:]
                        state = 'f_d'
                    else:
                        state = 'v_k'
                        tmp += string[0]
                        string = string[1:]

                elif state == 'v_k':
                    if string[0] in self.symbols:
                        if tmp.lower() in self.keywords: #大小写不敏感
                            result.append((tmp,self.bianma[tmp.lower()]))
                        else:
                            '''n = name(tmp)
                                self.name[tmp]=n'''
                            result.append((tmp,84))#变量名编码84

                        state = 'state0'
                        tmp = ''
                    else:
                        tmp +=string[0]
                        string = string[1:]

                elif state == 'f_d':
                    if string[0] in self.numbers:
                        if tmp[0] != '0':
                            tmp += string[0]
                            string = string[1:]
                        else:
                            print('int error')
                            break
                    elif string[0] == '.':

                        state = 'float'
                        tmp += string[0]
                        string = string[1:]
                    elif string[0] not in self.numbers and string[0] not in self.symbols:
                        print('error\n\n'+string)

                        result.append(('error',-1))
                        #break
                        state = 'state0'
                        tmp = ''
                        string = string[1:]
                    else:
                        result.append((int(tmp),82))#int编码82
                        state = 'state0'
                        tmp = ''

                elif state == 'float':
                    if string[0] in self.numbers:
                        tmp += string[0]
                        string = string[1:]
                    elif string[0] in self.symbols:
                        result.append((float(tmp),85)) #float编码85
                        state = 'state0'
                        tmp = ''
                    else:
                        print(tmp+'\nfloat error')
                        print('error\n\n' + string)

                        result.append(('error', -1))
                        # break
                        state = 'state0'
                        tmp = ''
                        string = string[1:]

                elif state == 'symbol':
                    if string[0] in self.symbols:
                        tmp += string[0]
                        if tmp == '/*':
                            result.append(('/*...*/',85))
                            tmp = ''
                            state = 'state0'
                            string = string[1:]
                        elif tmp in self.symbols:
                            result.append((tmp,self.bianma[tmp]))
                            tmp = ''
                            state = 'state0'
                            string = string[1:]
                        else:
                            result.append((tmp[0], self.bianma[tmp[0]]))
                            tmp = ''
                            state = 'state0'
                    else:
                        result.append((tmp,self.bianma[tmp]))
                        tmp = ''
                        state = 'state0'



                elif state == 'String':
                    if string[0]== '"' and tmp[-1] != '\\':
                        result.append((tmp,81))#string编码81
                        state = 'state0'
                        string = string[1:]
                        tmp =''
                    else:
                        tmp += string[0]
                        string = string[1:]

                elif state == 'Char':
                    if string[0] == "'":
                        result.append((tmp,80))#char编码80
                        tmp = ''
                        state = 'state0'
                        string = string[1:]
                    else:
                        if len(tmp) == 0:
                            tmp += string[0]
                            string = string[1:]
                        else:
                            if tmp == '\\' and string[0] in self.special:
                                tmp += string[0]
                                string = string[1:]
                            else:
                                print('Char error')
                                #break
                                print('error\n\n' + string)

                                result.append(('error', -1))
                                # break
                                state = 'state0'
                                tmp = ''
                                string = string[1:]

                elif state == 'sharp':
                    tmp += string[0]
                    string = string[1:]
        index = 0
        with open('results.txt','w') as f:

            for re in result:
                if index % 5 == 0:
                    f.write('\n')
                f.write('('+str(re[0])+','+str(re[1])+')')
                f.write('  ')
                index += 1



    def analyse(self,url):
        result = []
        with open(url,'r') as f:
            strings = ''
            for string in f.readlines():
                strings += string
            strings = self.deltetNote(strings)
        print(strings)
        self.DFA(strings,result)


if __name__ == '__main__' :
    lex = Lex()
    lex.analyse('test.c')



