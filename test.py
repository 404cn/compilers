def main():
    global ws
    cflag = 0  # 控制多行注释
    oflag = 0
    op_first = ''
    line = read_file('/Users/Desktop/test.c')
    # 行号
    line_num = 0
    # 多行注释起始行号
    line_comment_start = 0
    comment_start1 = '//'
    comment_start2 = '/*'
    comment_end = '*/'

    for i in line:
        # 去除空白行
        if len(i) < 1:
            line_num = line_num + 1
            continue
        else:
            #  处理注释行
            if cflag == 0:
                if i.startswith(comment_start1):  # 如果是以 // 开头
                    line_num = line_num + 1
                    continue
                elif i.startswith(comment_start2):  # 如果是以 /* 开头
                    line_comment_start = line_num
                    cflag = 1
                    line_num = line_num + 1
                    continue
            elif cflag == 1:
                if i.endswith(comment_end):  # 如果是以 */ 结尾
                    for m in range(line_comment_start, line_num + 1):
                        cflag = 0
                    line_num = line_num + 1
                    continue
                else:
                    line_num = line_num + 1
                    continue

            line_num = line_num + 1

        # 存放字符的列表
        each = []
        # 分解每个字符
        for m in i:
            each.append(m)  # 将每个字符添加到列表 each 中

        word = ''

        for e in each:
            # 是操作符
            if oflag == 1:
                if e in ['=', '<', '>', '+', '-', '*', '/', '%', '|', '&']:
                    OP_List.append(op_first + e)
                    print_List.append('Line:' + str(line_num) + ' ' +
                                      op_first + e + ', OP')
                    content_List.append(op_first + e)
                elif re.match(r'[a-zA-Z\_]', e):
                    word = word + e
                    OP_List.append(op_first)
                    print_List.append('Line:' + str(line_num) + ' ' +
                                      op_first + ', OP')
                    content_List.append(op_first)
                oflag = 0
                continue
            # 是常数 NUM
            elif oflag == 2:
                if e == ' ':
                    NUM_List.append(word)
                    print_List.append('Line:' + str(line_num) + ' ' + word +
                                      ', NUM')
                    content_List.append(word)
                    word = ''
                    oflag = 0
                elif e in SEPARATOR:
                    NUM_List.append(word)
                    print_List.append('Line:' + str(line_num) + ' ' + word +
                                      ', NUM')
                    content_List.append(word)
                    SEPARATOR_list.append(e)
                    print_List.append('Line:' + str(line_num) + ' ' + e +
                                      ', SEPARATOR')
                    content_List.append(e)
                    word = ''
                    oflag = 0
                else:
                    word = word + e
                continue
            # 是关键字或变量名
            elif oflag == 3:
                if e == ' ':
                    if word in key_ws:
                        KEY_List.append(word)
                        print_List.append('Line:' + str(line_num) + ' ' +
                                          word + ', KEY')
                        content_List.append(word)
                    elif re.match(ID, word):
                        ID_List.append(word)
                        print_List.append('Line:' + str(line_num) + ' ' +
                                          word + ', ID')
                        content_List.append(word)
                    word = ''
                    oflag = 0
                elif e in SEPARATOR:
                    if word in key_ws:
                        KEY_List.append(word)
                        print_List.append('Line:' + str(line_num) + ' ' +
                                          word + ', KEY')
                        content_List.append(word)
                    elif re.match(ID, word):
                        ID_List.append(word)
                        print_List.append('Line:' + str(line_num) + ' ' +
                                          word + ', ID')
                        content_List.append(word)
                    SEPARATOR_list.append(e)
                    print_List.append('Line:' + str(line_num) + ' ' + e +
                                      ', SEPARATOR')
                    content_List.append(e)
                    word = ''
                    oflag = 0
                else:
                    word = word + e
                continue
            # 是字符串 STRING
            elif oflag == 4:
                if e != '"':
                    word = word + e
                elif e == '"':
                    word = word + e
                    STRING_List.append(word)
                    print_List.append('Line:' + str(line_num) + ' ' + word +
                                      ', STRING')
                    content_List.append(word)
                    word = ''
                    oflag = 0
                continue

            # 判断是否是操作符（OP）
            if e in OP:
                oflag = 1
                op_first = e
                continue
            # 判断是否是分隔符（SEPARATOR）
            if e in SEPARATOR:
                SEPARATOR_list.append(e)
                print_List.append('Line:' + str(line_num) + ' ' + e +
                                  ', SEPARATOR')
                content_List.append(e)
                continue
            # 判断是否是常数 NUM
            if re.match(r'[0-9\.]', e):
                oflag = 2
                word = word + e
                continue
            # 判断是否是关键字或变量名
            if re.match(r'[a-zA-Z\_]', e):
                oflag = 3
                word = word + e
                continue
            # 判断是否是字符串
            if e == '"':
                oflag = 4
                word = word + e
                continue