import urllib.request
import re
from urllib.error import URLError,HTTPError
import os
import urllib.parse
import random
import http.client
import time
import socket
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
data = None
def open_url(url):
    request = urllib.request.Request(url,data,headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    return html
def get_proxy():
      url = 'http://www.xici.net.co'
      html = open_url(url)
      html = html.decode('utf-8')
      p = re.compile(r'''<tr\sclass[^>]*>\s+
                   <td\sclass[^>]*>.*?</td>\s+
                   <td>(.*?)</td>\s+
                   <td>(.*?)</td>\s+
                   <td>.*?</td>\s+
                   <td\sclass[^>]*>.*?</td>\s+
                   <td>(.*?)</td>''',re.X)                     
      proxies = p.findall(html)
      return proxies
def change_proxy(proxies):
      proxy_list = []
      for each in proxies:
            if each[2] == 'HTTP':
                  proxy_list.append(each[0]+':'+each[1])
      print('正在切换代理...')
      pp = urllib.request.ProxyHandler({'http':random.choice(proxy_list)})
      opener = urllib.request.build_opener(pp)
      opener.addheaders = [('User-Agent',headers['User-Agent'])]
      urllib.request.install_opener(opener)
def find_page(html):   #发现最大页数
      html = html.decode('utf-8')
      a = html.find('current-comment-page') + len('current-comment-page')+3
      b = html.find(']',a)
      return int(html[a:b])
def find_img(html):
      html = html.decode('utf-8')
      p = r'<img\ssrc="([^"]*\.(?:jpg|jpeg))"'
      imgs = re.findall(p,html)
      return imgs
def Down(fl='ooxx'):
      proxies = get_proxy()
      if os.path.isdir(fl):
            os.chdir(fl)
      else:
            os.mkdir(fl)
            os.chdir(fl)            
      page = 0
      imgs_addr = []
      while True:
            try:
                  if page == 0:
                        url = 'http://jandan.net/ooxx/'
                        html = open_url(url)
                        page = find_page(html)
                  else:
                      url = 'http://jandan.net/ooxx/'+'page-'+str(page)+'#comments'
                      html = open_url(url)
                      imgs = find_img(html)
                      print(imgs)
                      total = len(imgs)
                      for each in imgs:
                            each = 'http:'+each
                            filename = each.split('/')[-1]
                            urllib.request.urlretrieve(each,filename)
                            imgs_addr.append(each)
                            print('正在下载:',each)
                      imgs = []
                      page -= 1
                      print('总共下载了%d'%len(imgs_addr))
                      
            except HTTPError as e:
                  print('Error code:',e.code)                  
                  change_proxy(proxies)
                  continue
            except URLError as e:
                  print('Reason:',e.reason)                 
                  change_proxy(proxies)
                  continue
            except TimeoutError as t:
                print('Reason:',t)                
                change_proxy(proxies)
                continue
            except (ConnectionResetError,http.client.BadStatusLine) as e:
                print('Reason:',e)                
                change_proxy(proxies)
                continue
            except ConnectionResetError as e:
                print('Reason:',e)                
                change_proxy(proxies)
                continue
            except http.client.IncompleteRead as r:
                print('Reason:',r)               
                change_proxy(proxies)
                continue
            except socket.timeout as st:
                print('Reason:',st)
                change_proxy(proxies)
                continue
if __name__ == '__main__':   
      Down()

