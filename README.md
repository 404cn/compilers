# compilers

### 运行：
./compiler.py或./compiler.py ProgramFileName

### 文法的书写规则:
1.箭头请用符号→,空串请用符号ε
2.非终结符全大写，终结符全小写(单个英文字母作为非终结符除外)
    例:ALPHABET→A | B | C .... | x | y | z
3.产生式中各个非终结符，终结符和符号之间用空格隔开，如果用到'|'应该将含有非终结符的产生式写在前面
    例:OPERATIONEXPRESSION→TERM|+ TERM , OPERATIONEXPRESSION|- TERM , OPERATIONEXPRESSION
4.自行消除左递归，二意性(必须)与提取左公因式(非必须)

