import requests
import json
import pymysql
import threading

lock = threading.Lock()
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='zhuhuTopic',charset='utf8')
cursor = db.cursor()


def saveQuestionDB(id, title, url):
    # 插入数据
    lock.acquire()
    try:
        sql = "insert into questions values (%s,'%s','%s')" % (id, title, url)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    lock.release()


def saveArticleDB(id, title, vote, cmts, auth, url):
    # 插入数据
    lock.acquire()
    try:
        sql = "insert into article values (%s,'%s',%s,%s,'%s', '%s')" % (id, title, vote, cmts, auth, url)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    lock.release()


def fetchHotel(url):
    # 发起网络请求，获取数据
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }

    # 发起网络请求
    r = requests.get(url, headers=headers)
    r.encoding = 'Unicode'
    return r.text


def parseJson(text):
    json_data = json.loads(text)
    lst = json_data['data']
    nextUrl = json_data['paging']['next']

    if not lst:
        return;

    for item in lst:
        type = item['target']['type']

        if type == 'answer':
            # 回答
            question = item['target']['question']
            id = question['id']
            title = question['title']
            url = 'https://www.zhihu.com/question/' + str(id)
            print("问题：", id, title)
            # 保存到数据库
            saveQuestionDB(id, title, url)

        elif type == 'article':
            # 专栏
            zhuanlan = item['target']
            id = zhuanlan['id']
            title = zhuanlan['title']
            url = zhuanlan['url']
            vote = zhuanlan['voteup_count']
            cmts = zhuanlan['comment_count']
            auth = zhuanlan['author']['name']
            print("专栏：", id, title)
            # 保存到数据库
            saveArticleDB(id, title, vote, cmts, auth, url)

        elif type == 'question':
            # 问题
            question = item['target']
            id = question['id']
            title = question['title']
            url = 'https://www.zhihu.com/question/' + str(id)
            print("问题：", id, title)
            # 保存到数据库
            saveQuestionDB(id, title, url)
    return nextUrl


def crawl_1(topicID):
    url = 'https://www.zhihu.com/api/v4/topics/' + topicID + '/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id=0'
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


if __name__ == '__main__':
    topicID = '20192351'
    try:
        t1 = threading.Thread(target=crawl_1, args=(topicID,))
        t2 = threading.Thread(target=crawl_2, args=(topicID,))
        t3 = threading.Thread(target=crawl_3, args=(topicID,))
        t1.start()
        t2.start()
        t3.start()
    except:
        print("Error: 无法启动线程")