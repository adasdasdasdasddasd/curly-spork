PEDATA MAX 资讯
爬取的是24小时咨询，文章信息进行了加密，请求还需要用户的token
![image](./img/PEDATA1.png)
![image](./img/PEDATA2.jpg)   

经过跟栈找到加密位置会发现是一个gunzipSync函数，将数据压缩了，解压即可

![image](./img/PEDATA3.jpg)

请求时记得带上你自己的Token