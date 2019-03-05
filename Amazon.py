from collections import defaultdict
from collections import OrderedDict
import math
import re
import urllib3
from bs4 import BeautifulSoup as b

base_url = "https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
user_request = "shirt"

a1=300
b1=4.5

try:
    url = base_url + user_request
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    soup = b(r.data, "html.parser")

    count = 0
    list = []
    dict = {}
    newlist = []
    price_list = []

    for s in soup.find_all("li", attrs={"class": "celwidget"}):
        try:
            print((s.find_all("a", attrs={"class": "s-color-twister-title-link"})[0]).get('title'))
            list.append((s.find_all("a", attrs={"class": "s-color-twister-title-link"})[0]).get('title'))
        except:
            print("No Title for product")
            list.append("No Title for product")

        try:
            price = s.select("[class~=s-price]")[0].text[2:]
            print(s.select("[class~=s-price]")[0].text)
            if ("-" not in price):
                price = re.sub(r"[^0-9]", "", price)
                list.append(price)
            else:
                new_price = []
                for i in price.split("-"):
                    i = re.sub(r"[^0-9]", "", i)
                    new_price.append(i)
                sum = float(int(new_price[0]) + int(new_price[1])) / 2;
                list.append(price)

        except:
            try:
                price=s.select("[class~=s-size-mild]")[0].text
                print(s.select("[class~=s-size-mild]")[0].text)
                if ("-" not in price):
                    price = re.sub(r"[^0-9]", "", price)
                    list.append(price)
                else:
                    new_price = []
                    for i in price.split("-"):
                        i = re.sub(r"[^0-9]", "", i)
                        new_price.append(i)
                    sum = float(int(new_price[0]) + int(new_price[1])) / 2;
                    list.append(price)

            except:
                try:
                    price = s.select("[class~=acs_product-price__buying]")[0].text
                    print(s.select("[class~=acs_product-price__buying]")[0].text)
                    if ("-" not in price):
                        price = re.sub(r"[^0-9]", "", price)
                        list.append(price)
                    else:
                        new_price = []
                        for i in price.split("-"):
                            i = re.sub(r"[^0-9]", "", i)
                            new_price.append(i)
                        sum = float(int(new_price[0]) + int(new_price[1])) / 2;
                        list.append(price)

                except:
                    print("No price exists for the product")
                    list.append(3.6)

        try:
            k=s.find_all("span",attrs={"class":"a-icon-alt"}) #Rating
            if len(k) != 0:
                for i in k:
                    if (not(i.text == 'prime')):
                        rno = i.text
                        x = rno.split(" ")
                        rating = x[0]
                        print(rating)
                        list.append(rating)
                        print(" =============================================")
                    elif i.text == "prime" and (len(k) == 1):
                        print("No rating exists for the product")
                        list.append(3.6)
                        print(" =============================================")
                    else:
                        pass
            else:
                print("No rating exists for the product")
                list.append(3.6)
                print(" =============================================")
        except:
            print("No rating exists for the product");
            list.append(3.6)
            print(" =============================================")

        count = count + 1

    print(list)
    print(count)
    print(price_list)


    i = 0
    for element in list:
        newlist.append(element)
        list = list[1:]
        i = i + 1
        if i is 3:
            x = len(dict) + 1
            l = len(newlist)
            dict[x] = newlist[l-3:l]
            i = 0
    print(dict)

    length = len(dict)

    def cosine_similarity(v1,v2):
        if(len(v1)==len(v2)):
            sumxx, sumxy, sumyy = 0, 0, 0
            for i in range(len(v1)):
                x = v1[i]; y = v2[i]
                sumxx += x*x
                sumyy += y*y
                sumxy += x*y
        try:
            return sumxy/math.sqrt(sumxx*sumyy)
        except:
            return 0

    dict_angle={}
    sorted_angle=[]

    for k in range(length):
        cos = dict[k + 1]
        cos = cos[1:]
        int_cos=[]
        index=0
        for i in cos:
            int_cos.append(float(cos[index]))
            index=index+1
        angle = cosine_similarity([a1, b1], int_cos)
        dict[k+1].append(angle)
        dict_angle[k+1]=angle
        print(angle)

    sorted_angle=OrderedDict(sorted(dict_angle.items(), key=lambda t: t[1],reverse=True))
    print(sorted_angle)

    for i in sorted_angle:
         print(dict[i])
except:
    print("Please Check Your INTERNET Connection And Try Again")
    print("!!!!!HAPPY SHOPPING!!!!!!")
