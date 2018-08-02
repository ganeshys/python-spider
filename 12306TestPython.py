import requests
import passWord
import re
import random
import json
import pickle
import ssl
from urllib import parse
import time
ssl._create_default_https_context = ssl._create_unverified_context
# 伪装http请求
# url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.226728661343629'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/61.0'}

# # .text和.content的区别：取文本一般用.text 取图片一般用.content
# reponse = requests.get(url).content
# https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.6270023842993172
# https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.6320525817484169
# print(reponse)
#
# with open('captcha.jpg','wb') as f:
#     f.write(reponse)

# 自动处理会话
session = requests.session()

# def logig_12306():
login_urlaaaaaaa = 'https://kyfw.12306.cn/otn/login/init'
session.get(url=login_urlaaaaaaa,headers=headers)

def Verification():
    caotcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.7592617126025083'
    print(caotcha_url)
    print('下载验证码了')
    respond = session.get(url=caotcha_url,headers=headers)
    # 将二进制写入文件中
    with open('captcha.jpg', 'wb') as f:
        f.write(respond.content)



# 根据位置获取验证码
point = {
    '1':'37,46',
    '2':'111,46',
    '3':'181,46',
    '4':'254,46',
    '5':'37,116',
    '6':'111,116',
    '7':'181,116',
    '8':'254,116',
}
def get_arswer(index):
    index = index.split(',')
    temp = []
    for item in index:
        temp.append((point[item]))
    return ','.join(temp)


# 校检验证码
def check():
    # 传值字典
    data = {
    'answer':get_arswer(input('请输入序号验证码:')),
    'login_site':'E',
    'module':'login',
    'rand':'sjrand',
}
    check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    response = session.post(data=data,url=check_captcha_url,headers=headers)
    print(response.text)
    print('验证图片验证码了')
# 登录之后一系列的验证
def user_Login():
    data = {
    'appid':'otn',
    'password':passWord.passWord,
    'username':passWord.userName,
    }
    loginURL= 'https://kyfw.12306.cn/passport/web/login'
    response = session.post(url=loginURL,headers=headers,data=data)

    print(response.text)

def getjs():
    url = 'https://kyfw.12306.cn/otn/HttpZF/GetJS'
    r = session.get(url=url,headers=headers)
def post_uamauthclient():
    urlA = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
    data = {'appid': 'otn'}
    resPond=session.post(url=urlA, data=data, allow_redirects=False,headers=headers)
    newapptk = resPond.json()["newapptk"]
    resPond.encoding = 'utf-8'
    print(resPond.text)
    url = 'https://kyfw.12306.cn/otn/uamauthclient'
    data = {
        'tk': newapptk
    }
    r = session.post(url=url, data=data,headers=headers)
    apptk = r.json()["apptk"]
    r.encoding = 'utf-8'
    print(r.text)
def get_userLogin():
    url = 'https://kyfw.12306.cn/otn/login/userLogin'
    r = session.get(url=url,headers=headers)
    r.encoding = 'utf-8'

def get_leftTicket():
    url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    r = session.get(url=url,headers=headers)
    r.encoding = 'utf-8'
    # print(r.text)


def get_GetJS():
    url = 'https://kyfw.12306.cn/otn/HttpZF/GetJS'
    session.get(url=url,headers=headers)


def get_qufzjql():
    url = 'https://kyfw.12306.cn/otn/dynamicJs/qufzjql'
    session.get(url=url,headers=headers)

# 登录之后一系列的验证


# 获取数据
def shujuJeiKou():
    data_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9061'
    reponse = requests.get(data_url).text

    allStr = re.sub('[a-z@=\'_0-9;]', '', reponse).strip().split('|')

    # print(allStr)
    teamp = []
    for item in allStr:
        if item.strip():
            teamp.append(item)
    cotyName = []
    cotyCode = []
    a = 0
    print(teamp)
    for iseater in teamp:
        print(iseater)
        if a % 2 == 0:
            cotyName.append(iseater)
        else:
            cotyCode.append(iseater)
        a+=1

    print(cotyName)
    print(cotyCode)
    with open('citoCode_Name.pkl','wb') as f:
        pickle.dump(cotyName,f)
        pickle.dump(cotyCode,f)
# 这个方法只执行一次就OK
# shujuJeiKou()
def read_cityCode(city_name):
    a = 0
    with open('citoCode_Name.pkl','rb')as f:
        # 城市名
        myCity_Name = pickle.load(f)
        # 城市编码
        myCity_Code = pickle.load(f)

        # print(myCity_Name)

    for item in myCity_Name:
        if city_name == item:
            return myCity_Code[a]
        a+=1
    else:
        return ''



# print(read_cityCode(input('请输入您的出发地：')))
# print(read_cityCode(input('请输入您的目的地：')))

# https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-07-28&leftTicketDTO.from_station=ZZF&leftTicketDTO.to_station=SQF&purpose_codes=ADULT
# https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-07-28&leftTicketDTO.from_station=ZZF&leftTicketDTO.to_station=SQF&purpose_codes=ADULT
# https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-07-28&leftTicketDTO.from_station=ZZF&leftTicketDTO.to_station=SQF&purpose_codes=ADULT
# https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-07-24&leftTicketDTO.from_station=ZZF&leftTicketDTO.to_station=SQF&purpose_codes=ADULT

# 查询余票
def query_Ticket():
    origin = input('请输入您的出发地：')
    destination = input('请输入您的目的地：')
    dataTody = input('请输入日期：')
    print('查询列车了')
    query_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (dataTody,read_cityCode(origin),read_cityCode(destination))
    respond=session.get(url=query_url,headers = headers).text
    # print(respond)

    Dic_quer = json.loads(respond)
    # print(Dic_quer)
    # print(Dic_quer['data']['result'])
    trains_Arr= Dic_quer['data']['result']


    for iteam in trains_Arr:
        dandulist = str(iteam).split('|')
        # print(dandulist)
        if len(str(dandulist[0])) > 100 and str(dandulist[11])=='Y':
            # 这是高铁票 30,31,32(商务座)
            #大于100证明是有票的
            if str(dandulist[3])[:1]=='G':
                if str(dandulist[30]) == '有':
                    # urllib.parse.unquote()
                    # print(dandulist)
                    reservation_Ticket(DingDanHead=parse.unquote(str(dandulist[0])), date=dataTody, ChuFadi=origin,
                                       MuDidi=destination, fromStationTelecode=str(dandulist[6]),
                                       toStationTelecode=str(dandulist[7]), leftTict=str(dandulist[12]),
                                       stationTrainCode=str(dandulist[3]), train_on=str(dandulist[2]),
                                       train_location=str(dandulist[15]))

                    return
                    #有票，二等座
                elif str((dandulist[30])) == '无':
                    pass
                    #没有二等座位
                elif int((dandulist[30])) > 1:
                    # print(dandulist)
                    reservation_Ticket(DingDanHead=parse.unquote(str(dandulist[0])), date=dataTody, ChuFadi=origin,
                                       MuDidi=destination, fromStationTelecode=str(dandulist[6]),
                                       toStationTelecode=str(dandulist[7]), leftTict=str(dandulist[12]),
                                       stationTrainCode=str(dandulist[3]), train_on=str(dandulist[2]),
                                       train_location=str(dandulist[15]))

                    return
                    #有票，但余票不多
                else:
                    if str(dandulist[31]) == '有':
                        # print(dandulist)
                        reservation_Ticket(DingDanHead=parse.unquote(str(dandulist[0])), date=dataTody, ChuFadi=origin,
                                           MuDidi=destination, fromStationTelecode=str(dandulist[6]),
                                           toStationTelecode=str(dandulist[7]), leftTict=str(dandulist[12]),
                                           stationTrainCode=str(dandulist[3]), train_on=str(dandulist[2]),
                                           train_location=str(dandulist[15]))

                        return
                        # pass
                        # 有票，一等座
                    elif str((dandulist[31])) == '无':
                        pass
                        # 没有一等座
                    elif int((dandulist[30])) >=1:
                        # print(dandulist)
                        reservation_Ticket(DingDanHead=parse.unquote(str(dandulist[0])), date=dataTody, ChuFadi=origin,
                                           MuDidi=destination, fromStationTelecode=str(dandulist[6]),
                                           toStationTelecode=str(dandulist[7]), leftTict=str(dandulist[12]),
                                           stationTrainCode=str(dandulist[3]), train_on=str(dandulist[2]),
                                           train_location=str(dandulist[15]))

                        return
                        # pass
                        # 有票，但余票不多
                    else:
                        if str(dandulist[32]) == '有':
                            # print(dandulist)
                            reservation_Ticket(DingDanHead=parse.unquote(str(dandulist[0])), date=dataTody,
                                               ChuFadi=origin, MuDidi=destination,
                                               fromStationTelecode=str(dandulist[6]),
                                               toStationTelecode=str(dandulist[7]), leftTict=str(dandulist[12]),
                                               stationTrainCode=str(dandulist[3]), train_on=str(dandulist[2]),
                                               train_location=str(dandulist[15]))

                            return
                            # pass
                        # 有票，商务座
                        elif str((dandulist[32])) == '无':
                            pass
                        # 没有商务座
                        else:
                            # print(dandulist)
                            # fromStationTelecode,toStationTelecode,leftTict,stationTrainCode,train_location,train_on)
                            reservation_Ticket(DingDanHead=parse.unquote(str(dandulist[0])), date=dataTody, ChuFadi=origin,MuDidi=destination,fromStationTelecode=str(dandulist[6]),toStationTelecode=str(dandulist[7]),leftTict=str(dandulist[12]),stationTrainCode=str(dandulist[3]),train_on=str(dandulist[2]),train_location=str(dandulist[15]))

                            return
                            # pass
                         # 有票，但余票不多
            #
            # elif str(dandulist[3])[:1]=='K':
            #
            #     # 23(软卧)26（无座） 28(硬卧) 29(硬座)
            #     if str(dandulist[29]) == '有' or str(dandulist[29]) == '无':
            #         pass
            #     elif str(dandulist[23]) == '有'or str(dandulist[23]) == '无':
            #         pass
            #
            #     elif str(dandulist[26]) == '有'or str(dandulist[26]) == '无':
            #         pass
            #
            #     elif str(dandulist[28]) == '有'or str(dandulist[28]) == '无':
            #         pass
            #
            #     elif int(dandulist[29]) > 1:
            #         pass
            #
            #     elif int(dandulist[23]) > 1:
            #         pass
            #
            #     elif int(dandulist[26]) > 1:
            #         pass
            #
            #     elif int(dandulist[28]) >= 1:
            #         pass
                 #这是快车票
            else:
                pass
                #其他类型的车票（我暂时用不到~）


'''
G
[是否有票，预定，不知道是啥，车次，出发地，目的地，买票出发地，买票目的地，出发时间，到达时间，历时]
['', '预订', '38000G181305', 'G1816', 'ADF', 'AOH', 'ZAF', 'SQF', '10:23', '11:22', '00:59', 'N', '21ufbvxYwTmNja6tO6LHeiHg%2BuMkrU95ANDjrrMwA5IAFcDo', '20180725', '3', 'F1', '04', '06', '0', '0', '', '', '', '', '', '', '', '', '', '', '无', '无', '无', '', 'O0M090', 'OM9', '0'] 

['', '预订', '38000G187204', 'G1872', 'ZAF', 'HGH', 'ZAF', 'SQF', '10:56', '11:53', '00:57', 'N', '21ufbvxYwTmNja6tO6LHeiHg%2BuMkrU95ANDjrrMwA5IAFcDo', '20180725', '3', 'F1', '01', '03', '0', '0', '', '', '', '', '', '', '', '', '', '', '无', '无', '无', '', 'O0M090', 'OM9', '0']

['fzvEYiKISNolswNCh4wsdW79vlYS8Ss5JiZoMsoEJOd7OIV4m%2BmWueJ4xsSHbBicYSWRzIKaJDVA%0Ahz4rAQWsIy8NI5OPWhX%2FSGh8r08V6bRW%2BdaR9a4yd2CEbOSm25LZ6uwNfcOOCLOMRIGwY93s%2BuGi%0AOMCed5cLIW%2Bjjv4ASE8hFRMLq%2F8cAVCmMPqX62x6iUfuRolKendoGHnkgtZVnFrQJw7TpwcuZQi9%0A%2BD61CGI4k6GXk%2FpOa8JLey6hiHA5', '预订', '4f000G184406', 'G1844', 'EAY', 'RCK', 'ZAF', 'SQF', '10:35', '11:39', '01:04', 'Y', '8cwpNy%2BWJSVJTJYqCchOW3kVSAhiY6d%2FlH23Cx1JDHBTO8rd', '20180725', '3', 'Y2', '08', '10', '0', '0', '', '', '', '', '', '', '', '', '', '', '无', '无', '1', '', 'O0M090', 'OM9', '0']

['6Qzr4zWnbBLSh%2BASjal2Dx2wphqQAd9f8twjhy5BX4d0OKp58hj7KMHKHMvWUkfMJGwDv%2BuCLwfv%0ARf5hvNwwpwfwf1Mf8m74FC7XVSX97%2FMobcBBgDqYtzPP11ARpJNwMle8p4dvdHbxMzdIoQc%2B5EnL%0AEjPJKSTPfu2sq36HVJAGHbR3rfXHd3yTL6tHl0noyJp0iEOk6pF58iQjGVulb6zBTcCJiLQJdv04%0ADOtxW3nY2jhFpkj9wFyZf1E%3D', '预订', '6c0000G2880F', 'G288', 'CWQ', 'QDK', 'ZAF', 'SQF', '11:59', '12:57', '00:58', 'Y', '904SlvSL0W7rVOjaalDalSOgpKCoBc7dpI7xkcJ85%2BYrIdZL', '20180725', '3', 'Q7', '09', '11', '0', '0', '', '', '', '', '', '', '', '', '', '', '1', '有', '有', '', 'O0M090', 'OM9', '0']

['Sxt%2B%2FKubxlugy1cA1E7cJNlcUG4HUsyxkOGxzmEYduANSIws0hjl8hVSOkPNbrcILhKBmjhDvvr0%0AobP7O3DzGI%2FfxTz3y3tvaucpjiC%2B13qnA6iiq4rSLmtkMplxWGxkosZ0VNr2aNLggBVO8L1bo1x6%0A%2FN2ZOsWzEu0bEVBGxBN%2B%2BhEuqZBF42UqVqBc9u36j1MLTjsWJZRB1ZGd9%2F5Kd5%2BHEyFZsHDoQzdT%0AYtSWTfz0jM296jkOqVFEoG8%3D', '预订', '240000G80104', 'G804', 'BXP', 'SQF', 'ZAF', 'SQF', '12:04', '13:22', '01:18', 'Y', 'cttlTVnxexoCkRQp2n5EWRLdCza5wdPgjdLP1na0caNDsLqs', '20180725', '3', 'P2', '02', '06', '0', '0', '', '', '', '', '', '', '', '', '', '', '有', '有', '15', '', 'O0M090', 'OM9', '0']


['JX3nQWoXrttV25EOJiHQ4Pwc%2Fw4TyyJs5pYb0Srn%2FLGkFStRKWsX8If%2BDJNuzIn30UuNsuGAX14L%0AjXpIToRz43JR0jjs7RkT1sE2DEOfNt8Shmkd3hdfPfyUcNsuECdQvfjfNYvMB%2B8r3YuaKXJPV7%2FO%0AJg7tOXXKx6ny4qGoUpFVGQMnmmmTYhP8OAywj2gRlnBRJBlfeK0HuZWIU9GM1ZdXR89JaHpdQzZ6%0AGETrz3k3MpO0yf%2BDo6KpdrmKcUYC', '预订', '6c000G184804', 'G1848', 'CWQ', 'YAK', 'ZAF', 'SQF', '12:20', '13:17', '00:57', 'Y', 'OMkVvZWYCdBFG1%2FAPVElyCiEACb159agmnhv4aFSTSw6Ic7l', '20180725', '3', 'Q7', '07', '09', '0', '0', '', '', '', '', '', '', '', '', '', '', '1', '20', '12', '', 'O0M090', 'OM9', '0']
                                                          '二等''一等''商务'


K
['gxk%2BzMm%2FF04DLcAnzW%2B%2FKR5PSxHJN0n8%2FSjsol3H%2BPf9frsziD0C6u0MaBQOQvCCA%2BQSaI1ZNCP1%0AF0j8lfzRg94vu8PM3DiIhTZSROlYts%2Bc769sSKTMSVRrRTFBd%2Fz3ZJMOYyE27%2FQT8o1dqfbC46%2FT%0AsLNfofAyVn9W2mbzkQK%2FiuBqGejcxHHuovjOTnpcKrItKUcwE%2B%2B76gBEqx91OqpWCdBO%2BlfvTOHF%0A3wAi%2FgeK1ZnfV5w97gMCrvjYdnP39A0m%2FQ%3D%3D', '预订', '380000K7420L', 'K742', 'ZZF', 'XMS', 'ZZF', 'SQF', '12:45', '15:15', '02:30', 'Y', 'qG9jz%2BXKgFT2veE0DQOAMfvNZbwjR3CFGhwQS1mFnI%2Fc72BdzVWoyJe14gI%3D', '20180725', '3', 'F1', '01', '05', '0', '0', '', '', '', '10', '', '', '无', '', '有', '无', '', '', '', '', '10401030', '1413', '0']


['75Fjylumq%2B0bNywVOFUe7DFUmDpAwL3TuYIIxDJSkBccQJldOfzuhqV7RYbaPcWKspP7UPgNOKbK%0AzlpZlR8j9zEq5UM2eUPJyX0Kqpog7Q7w00%2Fp9rbEQQPReSsGZjzviryc1AGAjgItg48FO74lG8DJ%0A%2BnoZrMX1m8AE%2FRGrEem8BMU1x%2F15%2FTpoJPoX05gCpDalBnrGH2BVbPH1atYpuhca%2FvWyVvTQanJM%0AlZUUSGRtys9tcAHRflM9PjilYnuRFHcoMA%3D%3D', '预订', '38000K12400C', 'K1240', 'ZZF', 'RZH', 'ZZF', 'SQF', '12:33', '15:03', '02:30', 'Y', 'hbvr71WcF6B7AzipLLy4fKkIr7fgpVfX%2Bhwk4AkDMOc6zGVh4TxuUaZp6ew%3D', '20180725', '3', 'F1', '01', '05', '0', '0', '', '', '', '14', '', '', '无', '', '有', '无', '', '', '', '', '10401030', '1413', '0']
23(软卧)26（无座） 28(硬卧) 29(硬座)




['zj%2Bl2NYYKs%2B1qxiQVTTKOXFXK7z5ozvW0g5W9v%2Bn7tlnH%2B%2BDR3GZSit%2FVZwQtPfU5xusHASqphXI%0A%2BHjlVYsJqhmiP4yP7UGiqqov2yc1qiPl1MtrFH2fIRKPFqjqCgTJYv3ABxH6SOHK%2FhkmNjG6OUWc%0ArG%2Fbhqfl55yp%2ByIJOkMJSaw3BgQLCTu%2BoLfAgbKBKZMcP%2F1He93wiD28BcvFm7EuxlKzAFZETDh7%0AXOru6LiZFbA0lbC6rEnJMwmohYNFPrTAOQ%3D%3D', '预订', '93000K13520B', 'K1352', 'WAR', 'UKH', 'ZZF', 'SQF', '14:18', '17:00', '02:42', 'Y', 'VG5NAuws11z0LbSdiDoUEpzgFB%2FZeeXgcAzCp%2FBnIZg5yliOsUJ9DZ7YGbk%3D', '20180723', '3', 'R1', '25', '30', '0', '0', '', '', '', '2', '', '', '有', '', '3', '无', '', '', '', '', '10401030', '1413', '0']
23(软卧)26（无座） 28(硬卧) 29(硬座)

'''

# query_Ticket()


# 点击了预定
def reservation_Ticket(DingDanHead,date,ChuFadi,MuDidi,fromStationTelecode,toStationTelecode,leftTict,stationTrainCode,train_location,train_on):
    data = {
        '_json_att':'',
    }
#    请求一个检测登录的接口

    mofang_url ='https://kyfw.12306.cn/otn/login/checkUser'
    respond=session.post(url=mofang_url,data=data,headers=headers)
    # 验证登录
    print('验证登录了')
    # print(respond.text)
#     生成预订单的接口
    yuDindan_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    Y_data = {
        'back_train_date':date,
        'purpose_codes':'ADULT',
        'query_from_station_name':ChuFadi,
        'query_to_station_name':MuDidi,
        'secretStr':DingDanHead,
        'tour_flag':'dc',
        'train_date':date,
        'undefined':''
    }
    Yrespond=session.post(url=yuDindan_url,headers=headers,data=Y_data)
    print('点击预定了')
    # print(Y_data)

    # print('生成预订单结果如下:')
    # print(Yrespond.text)
    # def submit_order(date,fromStationTelecode,toStationTelecode,leftTict,stationTrainCode,train_location,train_on):

    submit_order(date=date,fromStationTelecode=fromStationTelecode,toStationTelecode=toStationTelecode,leftTict=leftTict,stationTrainCode=stationTrainCode,train_location=train_location,train_on=train_on)


def HuoQuUser():#获取密钥
    data = {
        '_json_att':''
    }
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    respond = session.post(url=url,data=data)
    print(respond.text)
    print('获取密钥了')
    REPEAT_SUBMIT_TOKEN = re.findall("globalRepeatSubmitToken = '(.*?)';", respond.text)[0]
    leftTickStr = re.findall("'leftTicketStr':'(.*?)'",respond.text)[0]
    east = '<script src="(.*?)" type="text/javascript" xml:space="preserve">'
    url_js = re.findall(east,respond.text)[0]
    # print(leftTickStr)
    # <script src="/otn/dynamicJs/obbspid" type="text/javascript" xml:space="preserve">
    # print(REPEAT_SUBMIT_TOKEN)
    url_js = 'https://kyfw.12306.cn%s'%(url_js)
    print(url_js)
    respond_js = session.get(url=url_js,headers=headers)
     # 发送一个js请求
    print('发送一个js请求')
    print(respond_js)



    # 请求一个js接口
    return REPEAT_SUBMIT_TOKEN,leftTickStr



def passGernss():
    leftTickStr,REPEAT_SUBMIT_TOKEN= HuoQuUser()

    # 获取乘客信息
    url_xinX = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    data_x = {
        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN,
        '_json_att': ''

    }
    r = session.post(url=url_xinX, data=data_x,headers=headers)
    r.encoding = 'utf-8'
    print('获取乘客信息了')
    # print(r.text)



    # 莫名其妙的验证码接口
    url_yanZhengMa = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&0.30257964274891924'
    yanzhengMa_resPond =session.get(url=url_yanZhengMa,headers=headers)
    print(yanzhengMa_resPond.text)

    return r.text,REPEAT_SUBMIT_TOKEN,leftTickStr

def submit_order(date,fromStationTelecode,toStationTelecode,leftTict,stationTrainCode,train_location,train_on):
    #
    # print('根据函数返回的乘客信息和密钥如下：')
    message,leftTickStr,REPEAT_SUBMIT_TOKEN = passGernss()
    # print('小夹子')
    # print(message)
    # print(REPEAT_SUBMIT_TOKEN)
    # print(leftTickStr)
    # 3e3f4f7d6d0a6a836e50fa3802f06798
    messag_dic= json.loads(message)
    if messag_dic['status'] == True:

        msg_des = messag_dic['data']['normal_passengers'][0]
        # print(msg_des)
        print('检查选票人信息了')

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        LeiXing= input('请输入坐席 高铁二等O一等M商务9,快车(硬卧:3硬座:1软卧:4):')
        data = {
            '_json_att': '',
            'bed_level_order_num': '000000000000000000000000000000',
            'cancel_flag': '2',
            'oldPassengerStr': '%s,1,%s,1_'%(msg_des['passenger_name'],msg_des['passenger_id_no']),
            'passengerTicketStr': '%s,0,1,%s,1,%s,%s,N'%(LeiXing,msg_des['passenger_name'],msg_des['passenger_id_no'],msg_des['mobile_no']),
            'randCode': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN,
            'tour_flag': 'dc',
            'whatsSelect': '1'
        }
        respond=session.post(url=url,headers=headers,data=data)

        # print(respond.text)
        # print(data)
        # Sat+Jul+28+2018+00:00:00+GMT+0800+(CST)
        # Tue+Jul+31+2018+00:00:00+GMT+0800+(CST)
        # 将日期时间转化为时间数组
        timeArray = time.strptime('00:00:00 %s' % (date), "%H:%M:%S %Y-%m-%d")
        # 将时间数组转换成格林时间
        geLin_time = time.strftime("%a %b %d %Y 00:00:00", timeArray)
        # print(type(geLin_time))
        all_date_str = '%s GMT 0800 (CST)' % (geLin_time)
        all_date_list = all_date_str.split(' ')
        endDate_str = '+'.join(all_date_list)
        # print(endDate_str)
        # Correlation Key: K7N2JRAIR5Q3PVF3JD7NN5KM
        queRenOrder_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        Order_data = {
            '_json_att': '',
            'fromStationTelecode':fromStationTelecode,
            'leftTicket': leftTickStr,
            'purpose_codes':'00',
            'REPEAT_SUBMIT_TOKEN':REPEAT_SUBMIT_TOKEN,
            'seatType':LeiXing,
            'stationTrainCode':stationTrainCode,
            'toStationTelecode':toStationTelecode,
            'train_date':endDate_str,
            'train_location':train_location,
            'train_no':train_on}
        # print('确认订单输出的参数如下：')
        print('点击提交了')

        # print(Order_data)
        order_proden = session.post(url=queRenOrder_url,data=Order_data,headers=headers)

        print('确认订单请求成功了，返回数据如下:')
        print(order_proden.text)



# 下载图片
Verification()
# 输入验证码
check()
# 登录
user_Login()
getjs()
post_uamauthclient()
get_userLogin()
get_leftTicket()
get_qufzjql()
get_GetJS()
# https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&0.6628760887560659
#
# 余票查询
query_Ticket()


# reservation_Ticket(DingDanHead='gKxSZza0xbwRv%2BbwxuTBMpmp0npOZX%2BAz2PrxPe25sEJxBv0%2Ft1v2RRh57HRaiowGmCNdJbyO7gv%0AzP%2FLoXeeUCvrhj7VBjn3CSBK8kGVWskmFhCm4cxpxdpNLKjpkdFrIsLHQXkQfVYmGSMvV%2BW5YwTD%0AntZFsZg%2FEVVN2wu4cdaWS5%2FphboymlY9oYteSjWKwQFrw8tNIFgkUc874VR9MqdVAzlIwEYuQO%2Fd%0AVql4nxJuR4hei59qyPXlzbDdp%2BZZ',date='2018-07-25',ChuFadi='郑州',MuDidi='商丘')