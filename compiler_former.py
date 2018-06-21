from Gram_SLR import SLR #语法语义分析，生成四元式
import Lex#词法分析器


#语法分析开始符号
start = 'A'
#语法分析文法
productions = {
    'A': ['V=E', ],
    'E': ['E+T', 'E-T', 'T'],
    'T': ['T*F', 'T/F', 'F'],
    'F': ['(E)', 'i'],
    'V': ['i', ],
}

if __name__ == '__main__' :
    lex = Lex()
    lex.analyse('Test.c')
