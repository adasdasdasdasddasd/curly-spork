# curly-spork
利用爬虫对知乎话题进行爬取，将页面的问题的问题爬取下来，存取到数据库。
使用多线程的方式来进行爬取，提高爬取效率。
打开知乎网页，按F12打开开发者工具，切换到 Network，过滤器选择 XHR。

![image](https://github.com/adasdasdasdasddasd/curly-spork/blob/main/%E6%8D%95%E8%8E%B7.PNG)

图中圈起来的地方是话题的 ID，如果后续大家想爬其他话题的话，只需要更改这个参数即可。
数据量较大，并且需要数据去重，所以为了省事儿，我决定使用 mysql 数据库来进行数据存储。
首先要安装 mysql 数据库，和 pymysql 库。
在 MySQL 数据库中创建数据库 zhuhuTopic 和数据表 questions，下面是我创建的表的结构。

![image](https://github.com/adasdasdasdasddasd/curly-spork/blob/main/3.PNG)


链接数据库：
import pymysql
db = pymysql.connect(host='xxx.xxx.xxx.xxx', port=3306, user='zhihuTopic', passwd='xxxxxx', db='zhihuTopic', charset='utf8')
cursor = db.cursor()
增删改查通过pymysql库操作数据库，实际上也是通过执行SQL语句。也就是说，自行构造 SQL 语句的字符串 sql，然后通过 *cursor.excute(sql) *执行。
查询数据时，执行 cursor.fetchone() 每次取一条数据，执行 cursor.fetchall() 一次性取全部数据，执行 cursor.fetchmany(n) 每次取 n 条数据。
python复制代码def insertDB(id, title, url):
    #插入数据
    try:
        sql = "insert into questions values (%s,'%s','%s')"%(id, title, url)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

 更新数据，删除数据等操作的写法跟插入数据的写法一样，只要修改对应 sql 语句即可。
使用多线程操作，每一个线程爬取一个页签的数据，提高爬虫效率。
def crawl_1(topicID):
    url = 'https://www.zhihu.com/api/v4/topics/' + topicID + '/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id=00'
    while url:
        text = fetchHotel(url)
        url = parseJson(text)
        print("crawl_1")

def crawl_2(topicID):
    url = 'https://www.zhihu.com/api/v4/topics/' + topicID + '/feeds/essence?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&offset=0'
    while url:
        text = fetchHotel(url)
        url = parseJson(text)
        print("crawl_2")

def crawl_3(topicID):
    url = 'https://www.zhihu.com/api/v4/topics/' + topicID + '/feeds/top_question?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&offset=0'
    while url:
        text = fetchHotel(url)
        url = parseJson(text)
        print("crawl_3")
        
我们将爬取讨论，精华，等待回答三个页签的代码，分别放到 crawl_1，crawl_2，crawl_3 这 3 个函数中。
然后在主函数中启动 3 条线程，每条线程执行一个爬虫函数。
python复制代码
def main():
    topicID = '20192351'
    try:
        t1 = threading.Thread(target=crawl_1, args=(topicID,))
        t2 = threading.Thread(target=crawl_2, args=(topicID,))
        t3 = threading.Thread(target=crawl_3, args=(topicID,))
        t1.start()
        t2.start()
        t3.start()
    except:
       print ("Error: 无法启动线程")

但是使用多线程的话，要注意一件事情，就是有些操作是可以多条线程同时做的，比如说发起网络请求，解析数据等，但是有些操作同一时间只能允许一条线程使用，比如说文件读写，数据库操作等。
所以，在数据库操作环节需要上锁，每次只放一个线程进去，避免多个线程同时操作数据库，造成错误。
python复制代码lock = threading.Lock()

def saveQuestionDB(id, title, url):
    #插入数据
    lock.acquire()
    try:
        sql = "insert into questions values (%s,'%s','%s')"%(id, title, url)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    lock.release()

在数据库操作之前 *lock.acquire() *上锁，操作完成之后，*lock.release() *解锁。

最后爬取结果如图所示，存储在数据库中：

![image](https://github.com/adasdasdasdasddasd/curly-spork/blob/main/2.PNG)
