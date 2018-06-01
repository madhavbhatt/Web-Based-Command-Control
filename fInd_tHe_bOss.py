import requests
import sys

bosses = []
it = 0
finance = 0
hr = 0
legal = 0
prodops = 0
marketing = 0
gtm = 0
cloud = 0
i = 0
# cloudinfra = 0

if len(sys.argv) != 2:
    print ("[*] usage : %s <username_file>" % sys.argv[0])
    sys.exit(-1)

with open(sys.argv[1]) as f:
    username = f.readlines()

content = [x.strip() for x in username]
f.close()


for username in content:
    i += 1
    print("for user no " + str(i) + " : " +str(username))
    try:
        req_1 = requests.get("https://my.netapp.com/wp-content/themes/wordpress-bootstrap-master/custom/cedAjaxRequest.php?q=" + username, timeout=10)
        data_1 = req_1.json()
        sup_num = data_1["PERSON"]["EMPLOYEE_NUM"]
        req_2 = requests.get("https://my.netapp.com/wp-content/themes/wordpress-bootstrap-master/custom/getManagementChain.php?supervisor=" + sup_num, timeout=10)
        data_2 = req_2.json()

        for boss in data_2["PERSON"]:
            bossName = boss["USERNAME"]
            bosses.append(bossName)
            # print (bossName)

        if 'millerw' in bosses:
            it += 1
        elif 'rpasek' in bosses:
            finance += 1
        elif 'gwenm' in bosses:
            hr += 1
        elif 'mfawcett' in bosses:
            legal += 1
        elif 'reich' in bosses:
            prodops += 1
        elif 'ejean' in bosses:
            marketing += 1
        elif 'henrir' in bosses:
            gtm += 1
        elif 'alye' in bosses:
            cloud += 1
        elif 'andb' in bosses:
            cloud += 1
    except:
        pass


    bosses = []


print("it : " + str(it))
print ("finance : " + str(finance))
print ("hr : " + str(hr))
print ("legal : " + str(legal))
print ("prodops : " + str(prodops))
print ("marketing : " + str(marketing))
print ("gtm : " + str(gtm))
print ("cloud : " + str(cloud))
# print ("cloudinfra : " + str(cloudinfra))
