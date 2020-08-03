import gspread_db
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import datetime

# You can learn more about how to register your
# service and get API credentials at:
# https://gspread.readthedocs.io/en/latest/oauth2.html
spreadsheet_key = '1jf3OrYadk3ACMPw4amB6PbTgDn90Wa1TL6H5nnGfGDo'

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)

client = gspread_db.authorize(credentials)
db = client.open_by_key(spreadsheet_key)

def get_noti_data():

    res = []

    DATA = db["Sheet1"]


    today = datetime.datetime.now()
    for i in DATA.get_all_records():
        TIME_LEFT = 0
        for k,v in i.items():

            if k == "ISSUE DATE" and v != "":
                format_str = '%d/%m/%Y' # The format
                datetime_obj = datetime.datetime.strptime(v, format_str)
                delta = datetime_obj - today
                # print(i["DWG NO"])
                TIME_LEFT = delta.days
                

            if not v == "":
                pass

        
        if i["ISSUE DATE"] != "":

            i["TIME_LEFT"] = TIME_LEFT
            res.append(i)


    res = sorted(res, key = lambda i: i['TIME_LEFT']) 


    datas = res

    data = [datas[x:x+8] for x in range(0, len(datas),8)]

    result = []

    for number,each in enumerate(data):

        data_to_noti = "📋รายงานแผนงานประจำวันที่ {} 📋 \n".format(str(datetime.datetime.now())[:10])
        data_to_noti_1_in = False
        data_to_noti_2_in = False

        data_to_noti_1 = "\n🥵เร่งมือหน่อย...\n"
        data_to_noti_2 = "\n😱สัปดาห์นี้มีส่งงาน....\n"

        for i in each:
            if 0 < int(i["TIME_LEFT"]) <= 3 :
                if int(i["PROGRESS"]) < 80:
                    data_to_noti_1_in = True
                    data_to_noti_1 += "\n👉อีก {} วัน ต้องส่ง {}\n🚧ความคืบหน้า{}%  \n🧍ผู้รับผิดชอบ {}\n".format(i["TIME_LEFT"],i["DWG NO."],i["PROGRESS"],i["OWNER"])
                
                else:
                    data_to_noti_1_in = True
                    data_to_noti_1 += "\n👉อีก {} วัน ต้องส่ง {}\n🟢ความคืบหน้า{}%  \n🧍ผู้รับผิดชอบ {} เยี่ยมมาก!\n".format(i["TIME_LEFT"],i["DWG NO."],i["PROGRESS"],i["OWNER"])
                


        for i in each:
            if 3 < int(i["TIME_LEFT"]) <= 7:

                try:
                    int(float(i["PROGRESS"])) < 30
                
                except:
                    continue

                if int(float(i["PROGRESS"])) < 30:
                    data_to_noti_2_in = True
                    data_to_noti_2 += "\n👉อีก {} วัน ต้องส่ง {}\n🚧ความคืบหน้า{}%  \n🧍ผู้รับผิดชอบ {}\n".format(i["TIME_LEFT"],i["DWG NO."],i["PROGRESS"],i["OWNER"])
                
                else:
                    data_to_noti_2_in = True
                    data_to_noti_2 += "\n👉อีก {} วัน ต้องส่ง {}\n🟢ความคืบหน้า{}%  \n🧍ผู้รับผิดชอบ {} เยี่ยมมาก!\n".format(i["TIME_LEFT"],i["DWG NO."],i["PROGRESS"],i["OWNER"])
        
        if data_to_noti_1_in:
            data_to_noti = data_to_noti + data_to_noti_1
            data_to_noti_1_in = False
            result.append(data_to_noti)

        if data_to_noti_2_in:
            data_to_noti = data_to_noti + data_to_noti_2
            data_to_noti_2_in = False
            result.append(data_to_noti)

    data_to_noti_3 = "\nกรุณาอัพเดต Progress ของงานได้ที่ \nhttps://bit.ly/3fHyqDt \nกดลิงค์นี้เพื่อตรวจสอบงานที่ต้องส่งภายในสัปดาห์ \nhttps://bit.ly/32utLRq"

    result.append(data_to_noti_3)
    return result

