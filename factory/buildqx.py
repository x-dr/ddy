# -*- coding: utf-8 -*-

import re
import time


# confs names in template/ and ../
# except sr_head and sr_foot
confs_names = [
    'qxproxy',
    'adqx'
]


def getRulesStringFromFile(path, kind):
    file = open(path, 'r', encoding='utf-8')
    contents = file.readlines()
    ret = ''

    for content in contents:
        content = content.strip('\r\n')
        if not len(content):
            continue

        if content.startswith('#'):
            ret += content + '\n'
        else:
            prefix = 'DOMAIN-SUFFIX'
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content):
                prefix = 'IP-CIDR'
                if '/' not in content:
                    content += '/32'
            elif '.' not in content:
                prefix = 'DOMAIN-KEYWORD'

            ret += prefix + ',%s,%s\n' % (content, kind)

    return ret


# get head and foot
str_head = open('template/sr_head.txt', 'r', encoding='utf-8').read()
str_foot = open('template/sr_foot.txt', 'r', encoding='utf-8').read()


# make values
values = {}

values['build_time'] = time.strftime("%Y-%m-%d %H:%M:%S")

# values['top500_proxy']  = getRulesStringFromFile('resultant/top500_proxy.list', 'Proxy')
# values['top500_direct'] = getRulesStringFromFile('resultant/top500_direct.list', 'Direct')

values['ad'] = getRulesStringFromFile('resultant/ad.list', 'Reject')

# values['manual_direct'] = getRulesStringFromFile('manual_direct.txt', 'Direct')
# values['manual_proxy']  = getRulesStringFromFile('manual_proxy.txt', 'Proxy')
# values['manual_reject'] = getRulesStringFromFile('manual_reject.txt', 'Reject')

values['gfwlist'] = getRulesStringFromFile('resultant/gfw.list', 'Proxy') \
                  + getRulesStringFromFile('manual_gfwlist.txt', 'Proxy')


# make confs
for conf_name in confs_names:
    file_template = open('template/'+conf_name+'.txt', 'r', encoding='utf-8')
    template = file_template.read()

    # template = str_head + template + str_foot

    file_output = open('../'+conf_name+'.list', 'w', encoding='utf-8')

    marks = re.findall(r'{{(.+)}}', template)

    print(marks,conf_name)

    for mark in marks:
        # print(mark)
        template = template.replace('{{'+mark+'}}', values[mark])

    file_output.write(template)
