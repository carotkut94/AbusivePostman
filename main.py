import random
import requests
import time
from notifypy import Notify

abusive_statements = ["The fu**ing order is still ", "Your life sucks, it is still ", "You know what, you should "
                                                                                      "rather die, because it is "
                                                                                      "still "]

notifier = Notify()


def get_package_details(track_no):
    try:
        header = {
            'Origin': 'https://www.fedex.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/59.0.3071.115 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8,fr;q=0.6,ta;q=0.4,bn;q=0.2'
        }

        data = {
            'action': 'trackpackages',
            'data': '{"TrackPackagesRequest":{"appType":"WTRK","appDeviceType":"DESKTOP","uniqueKey":"",'
                    '"processingParameters":{},"trackingInfoList":[{"trackNumberInfo":{"trackingNumber":"%s",'
                    '"trackingQualifier":"","trackingCarrier":""}}]}}' % (
                        str(track_no)),
            'format': 'json',
            'locale': 'en_US',
            'version': '1'
        }

        url = "https://www.fedex.com/trackingCal/track"
        response = requests.post(url, data=data, headers=header)

        if response.status_code == 200:
            print("response received successfully\n")
        else:
            print("request failed, error code : ", response.status_code)
            return

        res_json = response.json()

        if res_json['TrackPackagesResponse']['packageList'][0]['errorList'][0]['message'] != "":
            print(res_json['TrackPackagesResponse']['packageList'][0]['errorList'][0]['message'])
            return

        key_status = res_json['TrackPackagesResponse']['packageList'][0]['keyStatus']
        return key_status

    except Exception as e:
        print('Error occurred : \n Error Message: ' + str(e))


def push_status_notification(track_number):
    status = get_package_details(track_number)
    notifier.title = "AbusivePostman"
    notifier.message = abusive_statements[random.Random().randint(0, 2)] + status
    notifier.send()


tracking_number = 283482789967
push_status_notification(tracking_number)
half_hour = 30 * 60

while True:
    time.sleep(half_hour)
    push_status_notification(tracking_number)
