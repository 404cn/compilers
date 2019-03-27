#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "cJSON.h"


int lookup(char *);
FILE* open_file(char *, char *);
cJSON* parse_json();
void scaner(char *);
void out(int, char *);


// 用来存放单词
char TOKEN[50];


/*
 * c:相应单词的类别码
 * val:字母数字串 | 空串 | 数字串
 * 将类别码与相应的数据串以格式化的形式写入文件(追加到文件末尾并重置EOF)
 * 如果是保留字则只写入对应的编码, val为' '
 */
void out (int c, char *val) {
    FILE *fp = open_file("./Resault.txt", "at+");
    fprintf(fp, "(%d, %s)\n", c, val);
    fclose(fp);
}


/*
 * 按cJSON的格式序列化整个数据包
 * 成功则返回json结构体
 * 序列化失败程序退出（待改善）
 */
cJSON* parse_json () {
    FILE *fp = open_file("./scaner.json", "r");

    // 获得文件长度，然后讲文件指针恢复到开始处
    fseek(fp, 0, SEEK_END);
    long len = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    // 以数据块的形式读文件(1 * len)到开辟的内存空间中(data)
    char *data = (char *)malloc(len + 1);
    fread(data, 1, len, fp);
    // 已获得json文件数据，关闭文件
    fclose(fp);

    // 解析json数据
    cJSON *root = cJSON_Parse(data); // 将字符串解析成json结构体
    if (NULL == root) {
        printf("error : %s\n", cJSON_GetErrorPtr());
        cJSON_Delete(root);
        printf("press any key to exit ...\n");
        exit(1);
    }

    free(data);

    return root;
}


/*
 * str：需要查找单词分类码表的字符串
 * 若查到，返回相应的类别码
 * 否则返回0(标识符)
 */
int lookup (char *str) {
    int id = 0;
    cJSON *root = parse_json();
    
    if (NULL == (cJSON_GetObjectItem(root, str))) {
        return 0;
    }
    else
    {
        id = cJSON_GetObjectItem(root, str)->valueint;
        // 删除根节点，否则会出现内存泄露
        cJSON_Delete(root);
    }

    return id;
}


/*
 * file:需要打开的文件路径
 * 打开成功返回文件描述符
 * 失败则退出程序（待改善）
 */
FILE* open_file (char *file, char *mode) {
    FILE *fp;
    
    if (NULL == (fp = fopen(file, mode))) {
        printf("open file error, press any key to exit ...\n");
        getchar();
        exit(1);
    }

    return fp;
}


/*
 * file:需要进行词法分析的文件路径
 */
void scaner (char *file) {
    FILE *fp = open_file(file, "r");
    char ch;
    int i, c;
    while (EOF != (ch = fgetc(fp))) {
        if ((' ' == ch) || ('\n' == ch)) {
            continue;
        }
        if (isalpha(ch)) {
            TOKEN[0] = ch;
            ch = fgetc(fp);
            i = 1;
            while (isalnum(ch)) {
                TOKEN[i++] = ch;
                ch = fgetc(fp);
            }
            TOKEN[i] = '\0'; // 在单词末尾添加结束符
            fseek(fp, -1, 1); // 回退一个字符

            c = lookup(TOKEN);

            if (0 == c) {
                out(c, TOKEN);
            }
            else
            {
                out(c, " ");
            }
        }
        else
        {
            if (isdigit(ch)) {
                c = lookup("INT");
                TOKEN[0] = ch;
                ch = fgetc(fp);
                i = 1;
                while (isdigit(ch)) {
                    TOKEN[i++] = ch;
                    ch = fgetc(fp);
                }
                TOKEN[i] = '\0';
                fseek(fp, -1, 1);
                out(c, TOKEN);            
            }
            else
            {
                switch (ch)
                {
                    case '<':
                        ch = fgetc(fp);
                        if ('=' == ch) {
                            out(lookup("<="), "<=");
                        }
                        else
                        {
                            fseek(fp, -1, 1);
                            out(lookup("<"), "<");
                        }
                        break;
                    case '>':
                        ch = fgetc(fp);
                        if ('=' == ch) {
                            out(lookup(">="), ">=");
                        }
                        else
                        {
                            fseek(fp, -1, 1);
                            out(lookup(">"), ">");
                        }
                        break;
                    case '=':
                        ch = fgetc(fp);
                        if ('=' == ch) {
                            out(lookup("=="), "==");
                        }
                        else
                        {
                            fseek(fp, -1, 1);
                            out(lookup("="), "=");
                        }
                        break;
                    case '!':
                        ch = fgetc(fp);
                        if ('=' == ch) {
                            out(lookup("!="), "!=");
                        }
                        else
                        {
                            printf("错误：符号%c不在表中.\n", ch);
                            exit(1);
                        }
                        break;
                    case '/': 
                        ch = fgetc(fp);
                        if ('*' == ch) {
                            while (EOF != (ch = fgetc(fp))) {
                                if ((' ' == ch) || ('\n' == ch)) {
                                    continue;
                                }
                                if ('*' == ch) {
                                    if ('/' == (ch = fgetc(fp))) {
                                        break;       
                                    }
                                }
                            }
                        }
                        else if ('/' == ch) {
                            char *blackhole = (char *)malloc(82);
                            fgets(blackhole, 81, fp);
                            free(blackhole);
                        }
                        else {
                            out(lookup("/"), "/"); 
                        }
                        break;
                    case ',': out(lookup(","), ","); break;
                    case ';': out(lookup(";"), ";"); break;
                    case '(': out(lookup("("), "("); break;
                    case ')': out(lookup(")"), ")"); break;
                    case '{': out(lookup("{"), "{"); break;
                    case '}': out(lookup("}"), "}"); break;
                    case '+': out(lookup("+"), "+"); break;
                    case '-': out(lookup("-"), "-"); break;
                    case '*': out(lookup("*"), "*"); break;
                
                    default:
                        printf("错误：符号%c不在表中\n", ch);
                        exit(1);
                        break;
                }
            }
        }
    }
    fclose(fp);
    return;
}


int main (int argc, char* argv[]) {
    if (2 == argc) {
        scaner(argv[1]);
    }
    else
    {
        printf("请输入正确的格式!\n");
    }

    return 0;
}
