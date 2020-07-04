import requests
import json

class Session:
    def __init__(self, phone, pw):
        self.headers = {
          "X-Desktop-web": "1",
          'Origin': "https://bumble.com",
          'Referer': "https://bumble.com/get-started",
          "Sec-Fetch-Mode": "cors",
          "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
          "x-use-session-cookie": "1"
        }
        self.phone = phone
        self.pw = pw
        self.cookies = None
        self.login()

    def login(self):
        # get startup cookie
        url = 'https://bumble.com/mwebapi.phtml?SERVER_APP_STARTUP'
        data = '{"version":1,"message_type":2,"message_id":1,"body":[{"message_type":2,"server_app_startup":{"app_build":"MoxieWebapp","app_name":"moxie","app_version":"1.0.0","can_send_sms":false,"user_agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36","screen_width":1680,"screen_height":1050,"language":0,"is_cold_start":true,"external_provider_redirect_url":"https://bumble.com/static/external-auth-result.html?","locale":"en-us","app_platform_type":5,"app_product_type":400,"device_info":{"webcam_available":true,"form_factor":3},"build_configuration":2,"supported_features":[141,145,11,15,1,2,13,46,4,248,6,18,155,16,22,33,70,160,58,140,130,189,187,220,223,100,180,197,161,232,29,227,237,239,254],"supported_minor_features":[359,472,317,2,216,244,232,19,130,225,246,31,125,183,114,254,8,9,83,41,427,115,288,420,477,93,226,413,267,39,290,398,453,180,281,40,455,280,499,471,397,411,352,447,146,469,118,63,391,523,293,431,574,405,547],"supported_notifications":[83,73,3,72,46,109,81],"supported_payment_providers":[26,100,35,100001],"supported_promo_blocks":[{"context":92,"position":13,"types":[71]},{"context":89,"position":5,"types":[160,358]},{"context":8,"position":13,"types":[111,112,113]},{"context":53,"position":18,"types":[136,93,12]},{"context":45,"position":18,"types":[327]},{"context":45,"position":15,"types":[93,134,135,136,137,327,308,309,334]},{"context":10,"position":1,"types":[265,266]},{"context":148,"position":21,"types":[179,180,283]},{"context":130,"position":13,"types":[268,267]},{"context":113,"position":1,"types":[228]},{"context":3,"position":1,"types":[80]},{"context":3,"position":4,"types":[80,228]},{"context":119,"position":1,"types":[80,282,81,90]},{"context":43,"position":1,"types":[96,307]},{"context":10,"position":18,"types":[358]},{"context":10,"position":8,"types":[358]}],"supported_user_substitutes":[{"context":1,"types":[3]}],"supported_onboarding_types":[9],"user_field_filter_client_login_success":{"projection":[210,220,230,200,91,890,340,10,11,231,71,93,100]},"a_b_testing_settings":{"tests":[{"test_id":"bumble_web_boom_screen_opens_profile_xp"},{"test_id":"bumble__gifs_with_old_input"}]},"dev_features":["bumble_bizz","bumble_snooze","bumble_questions","bumble__pledge","bumble__request_photo_verification","bumble_moves_making_impact_","bumble__photo_verification_filters"],"device_id":"f94d310a-310a-0a34-340a-0a42fcb898cc","supported_screens":[{"type":23,"version":2},{"type":26,"version":0},{"type":13,"version":0},{"type":14,"version":0},{"type":15,"version":0},{"type":16,"version":0},{"type":17,"version":0},{"type":18,"version":0},{"type":19,"version":0},{"type":20,"version":0},{"type":21,"version":0},{"type":25,"version":0},{"type":27,"version":0},{"type":28,"version":0},{"type":57,"version":0},{"type":29,"version":1},{"type":69,"version":0},{"type":63,"version":0},{"type":92,"version":0},{"type":64,"version":0},{"type":65,"version":0},{"type":66,"version":0},{"type":67,"version":0}],"supported_landings":[{"source":25,"params":[20,3],"search_settings_types":[3]}]}}],"is_background":false}'
        resp_startup = requests.request("POST", url, data=data, headers=self.headers)
        url = 'https://bumble.com/mwebapi.phtml?SERVER_LOGIN_BY_PASSWORD'
        data = '{"version":1,"message_type":15,"message_id":12,"body":[{"message_type":15,"server_login_by_password":{"remember_me":true,"phone":"' + str(self.phone) + '","password":"' + self.pw + '","stats_data":""}}],"is_background":false}'
        resp = requests.request("POST", url, data=data, headers=self.headers, cookies=resp_startup.cookies)
        self.cookies = resp.cookies
        if 'form_failure' in resp.json()['body'][0]:
            raise Exception('Error at login')
    
    def get_encounters(self):
        try:
            url = 'https://bumble.com/mwebapi.phtml?SERVER_GET_ENCOUNTERS'
            data = '{"body":[{"message_type":81,"server_get_encounters":{"number":20,"context":1,"user_field_filter":{"projection":[210,370,200,230,490,540,530,560,291,732,890,930,662,570,380,493,1140,1150,1160,1161],"request_albums":[{"album_type":7},{"album_type":12,"external_provider":12,"count":8}],"game_mode":0,"request_music_services":{"top_artists_limit":8,"supported_services":[29],"preview_image_size":{"width":120,"height":120}}}}}],"message_id":81,"message_type":81,"version":1,"is_background":false}'
            resp_encounter = requests.request("POST", url, data=data, headers=self.headers, cookies=self.cookies)
            return self._parse_encounters(resp_encounter.json())
        except:
            print('No more encounters nearby')
            return dict()
        
    
    def get_full_user(self, user_id: str):
        url = 'https://bumble.com/mwebapi.phtml?SERVER_GET_USER'
        data = '{"body":[{"message_type":403,"server_get_user":{"user_id":"%s","user_field_filter":{"game_mode":0,"projection":[200,340,230,310,370,762,890,493,530,540,291,490,1160,1161,210,380],"request_music_services":{"top_artists_limit":10,"supported_services":[29]},"request_albums":[{"person_id":"%s","album_type":2,"offset":1},{"person_id":"%s","album_type":12,"external_provider":12}]},"client_source":10}}],"message_id":56,"message_type":403,"version":1,"is_background":false}'%(user_id,user_id,user_id)
        resp_user = requests.request("POST", url, data=data, headers=self.headers, cookies=self.cookies)
        return self._parse_full_user(resp_user.json())

    def _parse_full_user(self, resp_user):
        f_ud = resp_user['body'][0]['user']
        full_user = {k:v for k,v in f_ud.items() if k in ['user_id', 'name', 'age', 'gender', 'distance_long','distance_short']}
        try:
            full_user['hometown'] = f_ud['hometown']['city']['name']
            full_user['residence'] = f_ud['residence']['city']['name']
        except:
            pass
        
        full_user['images'] = []
        for album in f_ud['albums']:
            for photo in album.get('photos',[]):
                photo_data = {k:v for k,v in photo.items() if k in ['id', 'preview_url', 'large_url']} 
                photo_data['instagram'] = 'external_provider' in album
                full_user['images'].append(photo_data)

        return full_user


    def get_full_users(self):
        users = self.get_users()
        for user_id, user in users.items():
            user.update(self.get_full_user(user_id))
        return users

    def get_users(self):
        url = 'https://bumble.com/mwebapi.phtml?SERVER_GET_USER_LIST'
        data = '{"body":[{"message_type":245,"server_get_user_list":{"user_field_filter":{"projection":[200,210,340,230,640,580,300,860,280,590,591,250,700,762,592,880,582,930,585,583,305,330,763,1423,584,1262,911,912]},"preferred_count":30,"folder_id":0}}],"message_id":5,"message_type":245,"version":1,"is_background":false}'
        resp_user = requests.request("POST", url, data=data, headers=self.headers, cookies=self.cookies)
        return self._parse_users(resp_user.json())
  

    def _parse_encounter(self, ud_full):
        ud = ud_full['user']
        encounter = {k:v for k,v in ud.items() if k in ['user_id', 'name', 'age', 'gender',  'distance_long', 'distance_short','their_vote', 'access_level']}
        if 'profile_summary' in ud and 'primary_text' in ud['profile_summary']:
            encounter['profile_summary'] = ud['profile_summary']['primary_text']
        
        encounter['images'] = []
        for album in ud_full['albums']:
            for photo in album.get('photos',[]):
                photo_data = {k:v for k,v in photo.items() if k in ['id', 'preview_url', 'large_url']} 
                photo_data['instagram'] = 'external_provider' in album
                encounter['images'].append(photo_data)

        encounter['has_user_voted'] = ud_full['has_user_voted']
        return encounter

    def _parse_encounters(self, response):
        encounters = dict()
        for ud_full in response['body'][0]['client_encounters']['results']:
            encounter = self._parse_encounter(ud_full)
            encounters[encounter['user_id']] = encounter
        return encounters
    
    def _parse_users(self, response):
        tempting_users = dict()
        matched_users = dict()
        users = dict()
        for t_ud in response['body'][0]['client_user_list']['section'][0]['users']:
            tempting_users[t_ud['user_id']] = self._parse_temp_user(t_ud)
            users[t_ud['user_id']] = tempting_users[t_ud['user_id']]
            users[t_ud['user_id']]['tempting'] = True 
        for m_ud in response['body'][0]['client_user_list']['section'][1]['users']:
            matched_users[m_ud['user_id']] = self._parse_matched_user(m_ud)
            users[m_ud['user_id']] = matched_users[m_ud['user_id']]
            users[m_ud['user_id']]['tempting'] = False 
        return users
        
    def _parse_temp_user(self, t_ud):
        tempting_user = {k:v for k,v in t_ud.items() if k in ['user_id', 'name', 'age', 'gender', 'is_deleted', 'is_match', 'is_unread', 'online_status', 'is_extended_match', 'is_crush', 'online_status', 'their_vote_mode' ]}
        if tempting_user['is_match']:
            if 'pre_match_time_left' in tempting_user:
                tempting_user['pre_match_time_left'] = int(t_ud['pre_match_time_left']['goal']) - int(t_ud['pre_match_time_left']['progress'])
            else:
                tempting_user['pre_match_time_left'] = -1
        else:
            tempting_user['pre_match_time_left'] = 0
        tempting_user['images'] = [{k:v for k,v in t_ud['profile_photo'].items() if k in ['id', 'preview_url', 'large_url']}]       
        return tempting_user
    
    def _parse_matched_user(self, t_ud):
        matched_user = {k:v for k,v in t_ud.items() if k in ['user_id', 'name', 'age', 'gender', 'is_deleted', 'is_match', 'is_unread', 'online_status', 'is_extended_match', 'is_crush', 'online_status', 'their_vote_mode', 'unread_messages_count']}
        if matched_user['is_match']:
            if 'reply_time_left' in t_ud:
                matched_user['reply_time_left'] = int(t_ud['reply_time_left']['goal']) - int(t_ud['reply_time_left']['progress'])
            else:
                matched_user['reply_time_left'] = -1
        else:
            matched_user['reply_time_left'] = 0
        matched_user['images'] = [{k:v for k,v in t_ud['profile_photo'].items() if k in ['id', 'preview_url', 'large_url']}]       

        return matched_user

    #def get_chat(self, )


    def vote(self, user_id, like=False):
        url = 'https://bumble.com/mwebapi.phtml?SERVER_ENCOUNTERS_VOTE'
        vote = 2 if like else 3
        data = '{"body":[{"message_type":80,"server_encounters_vote":{"person_id":"'+user_id+'","vote":'+str(vote)+',"vote_source":1,"game_mode":0}}], "message_id":130,"message_type":80,"version":1,"is_background":false}'
        resp_vote = requests.request("POST", url, data=data, headers=self.headers, cookies=self.cookies)
        return resp_vote

    def vote_all(self, user_ids, like=False):
        for user_id in user_ids:
            self.vote(user_id, like)

    def update_location(self, lat, lon):
        url = 'https://bumble.com/mwebapi.phtml?SERVER_UPDATE_LOCATION'
        data = '{"body":[{"message_type":4,"server_update_location":{"location":[{"latitude":'+str(lat)+',"longitude":'+str(lon)+'}]}}],"message_id":13,"message_type":4,"version":1,"is_background":false}'
        resp_loc = requests.request("POST", url, data=data, headers=self.headers, cookies=self.cookies)
        return resp_loc

    def update_address(self, address):
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="b")
        location = geolocator.geocode(address)
        return self.update_location(location.latitude, location.longitude)

    
    