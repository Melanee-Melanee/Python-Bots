import requests
from errors.http_error import VoucherExceededException, PhoneInvalidException


class SnappTaxi:
    def __init__(self, user_number=None):
        self.user_number = user_number
        self.access_token = None
        self.session = requests.Session()


    def update_user_number(self, user_number):
        self.user_number = user_number

    def load_token(self):
       
        try:
            """
            To check the existence of the session file and whether the token has expired or not
            """

            with open(f'sessions/{self.user_number}_token.session', 'r') as f:
                self.access_token = f.read().strip()
                
                if self.access_token:

                    self.session.headers.update({
                        'authorization': f'Bearer {self.access_token}',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
                    })

                    """Checking the token validity."""
                    if self.checking_token_validity():
                        print("[+] Token was found and Token is valid")
                        return True
                    else:
                        print("[-] Token is invalid !")  
                        return False
                    

        except FileNotFoundError:
            print("[-] No token file found")
            self.access_token = None
            return False
        

    def send_sms(self):
        url = 'https://app.snapp.taxi/api/api-passenger-oauth/v2/otp'
        payload = {'cellphone': self.user_number}
        response = self.session.post(url, json=payload)
        response_json = response.json()

        if 'message' in response_json and response_json['message'] == 'not a valid cellphone':
            raise(PhoneInvalidException)


    """
    Checking the token validity.
    This function verifies the validity of the created session
        to prevent login if the session file has been tampered with. 
    """

    def checking_token_validity(self):

        url = 'https://app.snapp.taxi/api/api-base/v5/passenger/jek/content?lat=null&long=null'
        response = self.session.get(url)
        
        if response.json()['message'] == 'Unauthorized':    
            print("[-] The token is invalid")    
            return False   
        else:
            print("[+] The token is valid")
            return True

    def login(self, sms_code):
        url = 'https://app.snapp.taxi/api/api-passenger-oauth/v2/auth'
        payload = {
            'grant_type': 'sms_v2',
            'client_id': 'ios_sadjfhasd9871231hfso234',
            'client_secret': '23497shjlf982734-=1031nln',
            'cellphone': self.user_number,
            'token': sms_code,
            'referrer': 'pwa',
            'device_id': '3832c88d-6b17-4995-a592-ed8bf4ef9cc7',
            'secure_id': '3832c88d-6b17-4995-a592-ed8bf4ef9cc7',
        }
        response = self.session.post(url, json=payload)
        if response.status_code == 200:  
            response_json = response.json()
            

            with open(f'sessions/{self.user_number}_token.session', 'w') as f:
                f.write(response_json['access_token'])
            
            return True
        else:
            print(response.text)
            print("[-] There's a problem with the login !")
            return False


    def get_reward_id_by_name(self, name):

        url = 'https://snappclub.snapp.ir/api/v1/user/homepage/1'
        response = self.session.get(url)
        response_json = response.json()
        if response.status_code == 200 :
            for product in response_json['data']['homepage']['Products']:
                if name in product['name']:
                    return product['id']
            else:
                print("[-] 404 This coupon was not found :)")
                return False
        else:
            print(response.text)
            print("[-] An issue has occurred regarding the receipt of the prizes !")


    def redeem_prize(self, id):
        url = 'https://snappclub.snapp.ir/api/v1/user/voucher/redeem'
        params = {'product_id': id}
        response = self.session.post(url, json=params)


        if response.status_code == 200 and response.json()['data']['status'] != 'fail':
            print(f'[+] Voucher {id} redeemed successfully.')
        
        elif response.status_code == 403:
            raise(VoucherExceededException) 
        
        else:
            raise(RuntimeError)
            print('[-] Failed to redeem voucher.')
