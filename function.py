import json


def read_data():
    with open('cache.json', 'r', encoding='UTF-8') as f:
        data = json.loads(f.read())
    return data


def read_curent():
    with open('curent.txt', 'r', encoding='UTF-8') as f:
        name_nomal = f.readline().strip()
        name_weekend = f.readline().strip()
        name_nomal = name_nomal.split(',')
        name_weekend = name_weekend.split(',')
    return name_nomal, name_weekend


def write_data(data):
    with open('cache.json', 'w') as f:
        data = json.dumps(data)
        f.write(data)


def write_curent(name_nomal, name_weekend):
    r_nomal = ','.join(name_nomal) + "\n"
    r_weekend = ','.join(name_weekend)
    with open('curent.txt', 'w', encoding='utf-8') as f:
        f.write(r_nomal)
        f.write(r_weekend)


def update_date(sunday):
    with open('date_file.txt', 'w') as f:
        f.write(str(sunday))


def add_list(re_back, name_nomal, name_weekend, name_holiday):
    if re_back == '张旭辉':
        if '钟晓东' not in name_holiday:
            index1 = name_nomal.index('钟晓东')
            name_nomal.insert(index1, re_back)
        elif '邹堪芳' not in name_holiday:
            index1 = name_nomal.index('邹堪芳')
            name_nomal.insert(index1, re_back)
        elif '刘鹏辉' not in name_holiday:
            index1 = name_nomal.index('刘鹏辉')
            name_nomal.insert(index1, re_back)
        if '邹堪芳' not in name_holiday:
            index2 = name_weekend.index('邹堪芳')
            name_weekend.insert(index2, re_back)
        elif '苏伟健' not in name_holiday:
            index2 = name_weekend.index('苏伟健')
            name_weekend.insert(index2, re_back)
        elif '李琦学' not in name_holiday:
            index2 = name_weekend.index('李琦学')
            name_weekend.insert(index2, re_back)
    elif re_back == '钟晓东':
        if '邹堪芳' not in name_holiday:
            index1 = name_nomal.index('邹堪芳')
            name_nomal.insert(index1, re_back)
        elif '刘鹏辉' not in name_holiday:
            index1 = name_nomal.index('刘鹏辉')
            name_nomal.insert(index1, re_back)
        elif '王海涛' not in name_holiday:
            index1 = name_nomal.index('刘鹏辉')
            name_nomal.insert(index1, re_back)
        if '张旭辉' not in name_holiday:
            index2 = name_weekend.index('张旭辉')
            name_weekend.insert(index2, re_back)
        elif '邹堪芳' not in name_holiday:
            index2 = name_weekend.index('邹堪芳')
            name_weekend.insert(index2, re_back)
        elif '苏伟健' not in name_holiday:
            index2 = name_weekend.index('苏伟健')
            name_weekend.insert(index2, re_back)
    elif re_back == '邹堪芳':
        if '刘鹏辉' not in name_holiday:
            index1 = name_nomal.index('刘鹏辉')
            name_nomal.insert(index1, re_back)
        elif '王海涛' not in name_holiday:
            index1 = name_nomal.index('王海涛')
            name_nomal.insert(index1, re_back)
        elif '苏伟健' not in name_holiday:
            index1 = name_nomal.index('苏伟健')
            name_nomal.insert(index1, re_back)
        if '苏伟健' not in name_holiday:
            index2 = name_weekend.index('苏伟健')
            name_weekend.insert(index2, re_back)
        elif '李琦学' not in name_holiday:
            index2 = name_weekend.index('李琦学')
            name_weekend.insert(index2, re_back)
        elif '弯海峰' not in name_holiday:
            index2 = name_weekend.index('弯海峰')
            name_weekend.insert(index2, re_back)
    elif re_back == '刘鹏辉':
        if '王海涛' not in name_holiday:
            index1 = name_nomal.index('王海涛')
            name_nomal.insert(index1, re_back)
        elif '苏伟健' not in name_holiday:
            index1 = name_nomal.index('苏伟健')
            name_nomal.insert(index1, re_back)
        elif '李琦学' not in name_holiday:
            index1 = name_nomal.index('李琦学')
            name_nomal.insert(index1, re_back)
        if '王海涛' not in name_holiday:
            index2 = name_weekend.index('王海涛')
            name_weekend.insert(index2, re_back)
        elif '钟晓东' not in name_holiday:
            index2 = name_weekend.index('钟晓东')
            name_weekend.insert(index2, re_back)
        elif '张旭辉' not in name_holiday:
            index2 = name_weekend.index('张旭辉')
            name_weekend.insert(index2, re_back)
    elif re_back == '王海涛':
        if '苏伟健' not in name_holiday:
            index1 = name_nomal.index('苏伟健')
            name_nomal.insert(index1, re_back)
        elif '李琦学' not in name_holiday:
            index1 = name_nomal.index('李琦学')
            name_nomal.insert(index1, re_back)
        elif '弯海峰' not in name_holiday:
            index1 = name_nomal.index('弯海峰')
            name_nomal.insert(index1, re_back)
        if '钟晓东' not in name_holiday:
            index2 = name_weekend.index('钟晓东')
            name_weekend.insert(index2, re_back)
        elif '张旭辉' not in name_holiday:
            index2 = name_weekend.index('张旭辉')
            name_weekend.insert(index2, re_back)
        elif '邹堪芳' not in name_holiday:
            index2 = name_weekend.index('邹堪芳')
            name_weekend.insert(index2, re_back)
    elif re_back == '苏伟健':
        if '李琦学' not in name_holiday:
            index1 = name_nomal.index('李琦学')
            name_nomal.insert(index1, re_back)
        elif '弯海峰' not in name_holiday:
            index1 = name_nomal.index('弯海峰')
            name_nomal.insert(index1, re_back)
        elif '李泽杰' not in name_holiday:
            index1 = name_nomal.index('李泽杰')
            name_nomal.insert(index1, re_back)
        if '李琦学' not in name_holiday:
            index2 = name_weekend.index('李琦学')
            name_weekend.insert(index2, re_back)
        elif '弯海峰' not in name_holiday:
            index2 = name_weekend.index('弯海峰')
            name_weekend.insert(index2, re_back)
        elif '李泽杰' not in name_holiday:
            index2 = name_weekend.index('李泽杰')
            name_weekend.insert(index2, re_back)
    elif re_back == '李琦学':
        if '弯海峰' not in name_holiday:
            index1 = name_nomal.index('弯海峰')
            name_nomal.insert(index1, re_back)
        elif '李泽杰' not in name_holiday:
            index1 = name_nomal.index('李泽杰')
            name_nomal.insert(index1, re_back)
        elif '张旭辉' not in name_holiday:
            index1 = name_nomal.index('张旭辉')
            name_nomal.insert(index1, re_back)
        if '' not in name_holiday:
            index2 = name_weekend.index('弯海峰')
            name_weekend.insert(index2, re_back)
        elif '李泽杰' not in name_holiday:
            index2 = name_weekend.index('李泽杰')
            name_weekend.insert(index2, re_back)
        elif '刘鹏辉' not in name_holiday:
            index2 = name_weekend.index('刘鹏辉')
            name_weekend.insert(index2, re_back)
    elif re_back == '':
        if '李泽杰' not in name_holiday:
            index1 = name_nomal.index('李泽杰')
            name_nomal.insert(index1, re_back)
        elif '张旭辉' not in name_holiday:
            index1 = name_nomal.index('张旭辉')
            name_nomal.insert(index1, re_back)
        elif '钟晓东' not in name_holiday:
            index1 = name_nomal.index('钟晓东')
            name_nomal.insert(index1, re_back)
        if '李泽杰' not in name_holiday:
            index2 = name_weekend.index('李泽杰')
            name_weekend.insert(index2, re_back)
        elif '刘鹏辉' not in name_holiday:
            index2 = name_weekend.index('刘鹏辉')
            name_weekend.insert(index2, re_back)
        elif '王海涛' not in name_holiday:
            index2 = name_weekend.index('王海涛')
            name_weekend.insert(index2, re_back)
    elif re_back == '李泽杰':
        if '张旭辉' not in name_holiday:
            index1 = name_nomal.index('张旭辉')
            name_nomal.insert(index1, re_back)
        elif '钟晓东' not in name_holiday:
            index1 = name_nomal.index('钟晓东')
            name_nomal.insert(index1, re_back)
        elif '邹堪芳' not in name_holiday:
            index1 = name_nomal.index('邹堪芳')
            name_weekend.insert(index1, re_back)
        if '刘鹏辉' not in name_holiday:
            index2 = name_weekend.index('刘鹏辉')
            name_weekend.insert(index2, re_back)
        elif '王海涛' not in name_holiday:
            index2 = name_weekend.index('王海涛')
            name_weekend.insert(index2, re_back)
        elif '钟晓东' not in name_holiday:
            index2 = name_weekend.index('钟晓东')
            name_weekend.insert(index2, re_back)
