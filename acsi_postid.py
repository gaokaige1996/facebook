from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import re
from random import randint
from time import sleep


#match reply with comments
def commentid(driver,id):
    length = -1
    comments = []
    while len(comments) > length:
        length = len(comments)
        sleep(randint(10, 20))
        comments = driver.find_elements_by_xpath('//*[@id="'+str(id)+'"'+']/div[2]/div/div[3]/div/div')
        #print(length,len(comments))
        return comments


#obtain reply user id and reply user name
def replyinfo(driver,id,n):
    replyidlist = driver.find_elements_by_xpath('//*[@id="' + str(id) + '"' + ']/div[2]/div/div[3]/div/div['+str(n)+']/div[@aria-label="Comment reply"]')
    replyuidl = []
    replynamel = []
    replywordsl = []
    for i in replyidlist:
        replyid = i.get_attribute('id')
        replyuid = driver.find_element_by_xpath('//*[@id="'+str(replyid)+'"]/div/div/div/div[1]/a').get_attribute('data-hovercard')
        replyuid = int(re.findall(r"\d\d\d\d+", replyuid)[0])
        replyname = driver.find_element_by_xpath('//*[@id="'+str(replyid)+'"]/div/div/div/div[1]/a/img').get_attribute('alt')
        #replywords = driver.find_elements_by_xpath('//*[@id="'+str(replyid)+'"]/div/div/div/div[2]/div/div/div[1]/div[1]/div/span/span[2]/span/span/span')
        replywords = driver.find_elements_by_xpath('//*[@id="'+str(replyid)+'"]/div/div/div/div[2]/div/div/div[1]/div[1]')
        words = []
        word10 = []
        for i in replywords:
            word = i.text
            word = word.replace("\n", "")
            words.append(word)

        for m in words:
            g = m.split(' ')
            for t in g:
                word10.append(t)

        replynamelsing = replyname.split(' ')
        lenreplyname = len(replynamelsing)
        word10 = word10[lenreplyname:]
        if len(word10) >= 1 and word10[-1][-1].isdigit():
            lastword = word10[-1][:-1]
            word10 = word10[:-1]
            word10.append(lastword)
            word10 = word10[:10]
        else:
            word10 = word10[:10]
        word10 = [' '.join(word10)][0]
        word10 = word10[:10]
        replywordsl.append(word10)
        #print(replyid,replyuid,replyname)
        replyuidl.append(replyuid)
        replynamel.append(replyname)
    return replyuidl,replynamel,replywordsl


def final(fileid,postid):
#####################driver 地址#####################3
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2,"permissions.default.stylesheet":2,"javascript.enabled":False,"profile.default_content_setting_values.notifications":1}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('https://www.facebook.com')
# if has other windows

    #driver.find_element_by_id("expanding_cta_close_button").click()

#not have other windows

    driver.find_element_by_id("email").clear()
    driver.find_element_by_id("email").send_keys('fanyu@onid.oregonstate.edu')
#account:fanyu@onid.oregonstate.edu
#password:Kaige199678
#gaokaige1996@gmail.com
#gaokaige960523
    driver.find_element_by_id("pass").clear()
    driver.find_element_by_id("pass").send_keys('Kaige199678')
    driver.find_element_by_id("loginbutton").click()

    driver.get('https://www.facebook.com/'+fileid+'/posts/'+postid)


    sleep(randint(5, 10))
    #弹窗
    try:
        driver.find_element_by_xpath('//*[@id="photos_snowlift"]/div[2]/div/a').click()
    except:
        pass

    #obtain "post_id"
    posts= driver.find_element_by_xpath('//form[@method="post"]')
    id = posts.get_attribute('id')
    #print(id)

    #click view more comments
    numdiv = driver.find_elements_by_xpath('//*[@id="'+str(id)+'"'+']/div[2]/div/div[3]/div/div')
    #print(len(numdiv))

    try:
        driver.find_element_by_xpath('//*[@id="'+str(id)+'"'+']/div[2]/div/div[3]/div/div['+str(len(numdiv))+']/div/div[2]/a').click()
        sleep(randint(5, 10))
    except:
        print('No view more comments')


    #view more replies
    try:
        for i in driver.find_elements_by_css_selector('a.UFIPagerIcon.img._8o._8r.UFIImageBlockImage'):
            driver.execute_script("arguments[0].click();", i)
            sleep(randint(2,5))

        sleep(randint(5, 10))
    except:
        print('No view more replies')
    #view n replies
    try:
        for i in driver.find_elements_by_css_selector('span.UFIReplySocialSentenceLinkText.UFIReplySocialSentenceVerified'):
            driver.execute_script("arguments[0].click();", i)
            sleep(randint(2, 5))
        sleep(randint(5, 10))
    except:
        print('No view n replies')
    #view n more replies again
    try:
       for i in driver.find_elements_by_css_selector('a.UFIPagerIcon.img._8o._8r.UFIImageBlockImage'):
           driver.execute_script("arguments[0].click();", i)
           sleep(randint(2, 5))
       sleep(randint(5, 10))
    except:
        print('No view more replies again')


    comments = commentid(driver,id)
    comments = comments[:-1]

    n = 0

    with open(str(fileid)+'_'+str(postid) + '.txt', 'w') as f:
        for i in comments:
            #comments include reply id and comment id
            classname = i.get_attribute('class')
            commentsid =i.get_attribute('id')
            if n+2 <= len(comments):
                nextclassname = comments[n+1].get_attribute('class')
            else:
                nextclassname = None
            if classname == ' UFIReplyList':
                reply_cid = comments[n-1].get_attribute('id')
                userid = driver.find_element_by_xpath('//*[@id="' + str(reply_cid) + '"]/div/div/div/div[1]/a').get_attribute(
                    'data-hovercard')
                userid = int(re.findall(r"\d\d\d\d+", userid)[0])

                # comment user name
                username = driver.find_element_by_xpath(
                    '//*[@id="' + str(reply_cid) + '"]/div/div/div/div[1]/a/img').get_attribute('alt')

                # comment character 20
                commentword = driver.find_elements_by_xpath(
                    '//*[@id="' + str(reply_cid) + '"]/div/div/div/div[2]/div/div/div[1]/div[1]')
                words = []
                word20 = []
                for w in commentword:
                    word = w.text
                    word = word.replace("\n", "")
                    words.append(word)

                for m in words:
                    g = m.split(' ')
                    for t in g:
                        word20.append(t)
                usernamel = username.split(' ')
                lenusername = len(usernamel)
                word20 = word20[lenusername:]
                if len(word20) >= 1 and word20[-1][-1].isdigit():
                    lastword = word20[-1][:-1]
                    word20 = word20[:-1]
                    word20.append(lastword)
                    word20 = word20[:20]
                else:
                    word20 = word20[:20]
                word20 = [' '.join(word20)][0]
                #first 20 character
                word20 = word20[:20]

                # print(word20)
                m = n+1
                replyuidl, replynamel,replyword10l = replyinfo(driver,id,m)
                for g in range(len(replyuidl)):
                    #print(reply_cid, username, userid, word20, replynamel[g], replyuidl[g],replyword10l[g])
                    f.write(str(reply_cid) + ' | ' + username + ' | ' + str(userid) + ' | ' + word20 + ' | ' + replynamel[g] + ' | ' + str(replyuidl[g]) + ' | ' +replyword10l[g]+'\n')


            elif classname != ' UFIReplyList' and nextclassname != ' UFIReplyList':
                reply_cid = comments[n].get_attribute('id')

                #change content to repy_cid
                userid = driver.find_element_by_xpath('//*[@id="' + str(reply_cid) + '"]/div/div/div/div[1]/a').get_attribute(
                    'data-hovercard')
                userid = int(re.findall(r"\d\d\d\d+", userid)[0])

                # comment user name
                username = driver.find_element_by_xpath(
                    '//*[@id="' + str(reply_cid) + '"]/div/div/div/div[1]/a/img').get_attribute('alt')

                # comment character 20
                commentword = driver.find_elements_by_xpath(
                    '//*[@id="' + str(reply_cid) + '"]/div/div/div/div[2]/div/div/div[1]/div[1]')
                words = []
                word20 = []
                for w in commentword:
                    word = w.text
                    word = word.replace("\n", "")
                    words.append(word)

                for m in words:
                    g = m.split(' ')
                    for t in g:
                        word20.append(t)
                usernamel = username.split(' ')
                lenusername = len(usernamel)
                word20 = word20[lenusername:]
                if len(word20) >= 1 and word20[-1][-1].isdigit():
                    lastword = word20[-1][:-1]
                    word20 = word20[:-1]
                    word20.append(lastword)
                    word20 = word20[:20]
                else:
                    word20 = word20[:20]
                word20 = [' '.join(word20)][0]
                #first 20 character
                word20 = word20[:20]

                #print(reply_cid, username, userid, word20, None, None,None)
                f.write(str(reply_cid) + ' | ' + username + ' | ' + str(userid) + ' | ' + word20 + ' | ' + 'None' + ' | ' + 'None' + ' | ' + 'None' + '\n')

            n = n+1
    driver.quit()


file = open("acsi_postid.txt")

with open('Error.txt','w') as f:
    for line in file.readlines():
        line=line.strip('\n')
        l = line.split('  ')
        fileid = l[0]
        postid = l[1]
        try:
            final(fileid,postid)
            print(fileid,postid,'is finished')
        except:
            f.write(fileid + '  '+postid + '\n')
            print('-----------------------')
            print('Error!!!WTF',fileid,postid)
            print('-----------------------')
