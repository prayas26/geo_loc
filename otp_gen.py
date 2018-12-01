import httplib
import key

otp_key = key.msg91_key

def sendsms(mobile, otp):
    print(otp_key)
    conn = httplib.HTTPConnection("api.msg91.com")
    sms = "/api/sendhttp.php?sender=BLUHCK&route=4&mobiles="+mobile+"&authkey="+otp_key+"&country=91&message=Namaste! Thanks for registering for Blu. Your OTP is "+otp+". Enter this to complete your registration. Dhanyawaad!"
    print(sms)
    print(conn.request("GET", sms))

def new_request(mobile, un_id):
    print(otp_key)
    conn = httplib.HTTPConnection("api.msg91.com")
    sms = "/api/sendhttp.php?sender=BLUHCK&route=4&mobiles="+mobile+"&authkey="+otp_key+"&country=91&message=Namaste! Thanks for creating a new request and helping us make India clean. Your unique id is "+un_id+". Dhanyawaad!"
    print(sms)
    print(conn.request("GET", sms))