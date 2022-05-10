# -*- coding: utf-8 -*-

#
# 提取广告规则，并且只提取对全域禁止的那种规则
#

# 参考 ADB 广告规则格式：https://adblockplus.org/filters

import time
import sys
import requests
import re


rules_url = [
    # EasyList China
    # 'https://easylist-downloads.adblockplus.org/easylistchina.txt',
    # EasyList + China
    'https://easylist-downloads.adblockplus.org/easylistchina+easylist.txt',
    # 乘风 广告过滤规则
    # 'https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/ABP-FX.txt'
    'https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt',
    'https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt',
    # anti-AD
    'https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt',
    # adblock_list
    'https://raw.githubusercontent.com/uniartisan/adblock_list/master/adblock.txt',
    # 可从国际网页上删除大部分广告，包括不需要的框架，图像和对象
    # EasyList
     'https://easylist-downloads.adblockplus.org/easylist.txt',
    #  EasyList China EasyList 的中文补充过滤器
    'https://easylist-downloads.adblockplus.org/easylistchina.txt',
    # EasyPrivacy
    # 可选的补充过滤器列表，该列表从网络删除了所有形式的跟踪，包括 Web 错误，跟踪脚本和信息收集器，从而保护您的个人数据
    'https://easylist-downloads.adblockplus.org/easyprivacy.txt',
    # EasyList Cookie List
    # 阻止 cookie 横幅，GDPR 覆盖窗口和其他与隐私相关的通知
    # 'https://easylist-downloads.adblockplus.org/easylist-cookie.txt', 
    # CJX's Annoyance List
    # “ EasyList China + EasyList” 和 “ EasyPrivacy” 的补充，删除了中文网站上的烦人的自我推广
    'https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt',
    # 可从几乎所有网站上删除 Cookie 警告，并为您节省数千次不必要的点击！
    # I don't care about cookies
    'https://www.i-dont-care-about-cookies.eu/abp/',
    # halflife
    'https://github.com/o0HalfLife0o/list/blob/master/ad.txt',
    # Hblock
    # 通过阻止广告，跟踪和恶意软件域来提高安全性和隐私性
    'https://hblock.molinero.dev/hosts',
    # 您可以使用此文件来阻止广告，横幅，第三方 Cookie，第三方页面计数器，网络错误，甚至是大多数劫持和可能有害的程序
    # Mvps
    'http://winhelp2002.mvps.org/hosts.txt'








]

rule = ''

# contain both domains and ips
domains = []


for rule_url in rules_url:
    print('loading... ' + rule_url)

    # get rule text
    success = False
    try_times = 0
    r = None
    while try_times < 5 and not success:
        r = requests.get(rule_url)
        if r.status_code != 200:
            time.sleep(1)
            try_times = try_times + 1
        else:
            success = True
            break

    if not success:
        sys.exit('error in request %s\n\treturn code: %d' %
                 (rule_url, r.status_code))

    rule = rule + r.text + '\n'


# parse rule
rule = rule.split('\n')
for row in rule:
    row = row.strip()
    row0 = row

    # 处理广告例外规则

    if row.startswith('@@'):
        i = 0
        while i < len(domains):
            domain = domains[i]
            if domain in row:
                del domains[i]
            else:
                i = i + 1

        continue

    # 处理广告黑名单规则

    # 直接跳过
    if row == '' or row.startswith('!') or "$" in row or "##" in row:
        continue

    # 清除前缀
    row = re.sub(r'^\|?https?://', '', row)
    row = re.sub(r'^\|\|', '', row)
    row = row.lstrip('.*')

    # 清除后缀
    row = row.rstrip('/^*')
    row = re.sub(r':\d{2,5}$', '', row)  # 清除端口

    # 不能含有的字符
    if re.search(r'[/^:*]', row):
        print('ignore: '+row0)
        continue

    # 只匹配域名或 IP
    if re.match(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,9}$', row) or re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', row):
        domains.append(row)

print('done.')


# write into files

file_ad = sys.stdout
try:
    if sys.version_info.major == 3:
        file_ad = open('resultant/ad.list', 'w', encoding='utf-8')
    else:
        file_ad = open('resultant/ad.list', 'w')
except:
    pass

file_ad.write('# adblock rules refresh time: ' +
              time.strftime("%Y-%m-%d %H:%M:%S") + '\n')

domains = list(set(domains))
domains.sort()

for item in domains:
    file_ad.write(item + '\n')
