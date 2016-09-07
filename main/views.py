from django.shortcuts import render
import json, requests, random, re
from pprint import pprint
import json
from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
import urlparse
import requests
import json
youtube_api_key = 'AIzaSyCwfYr2kH1prDPTXMKPDUGAsJMfzTz-x2c'
access_token = 'EAAQEBiZBEdF0BAEUVSA4tckX8JnBTlhcOThVa9B1G581SyxEUZB5hWVhQvifBwac8iyrZCmpuZBMyXSsLXyHHhtQhpmZC99JvWQJ2gmoUqX1dID4g54MBeQiZB7e2jMGaJK2UzGxuSNdEz1hRoi4FZAteqtBGGBVbzQ6gZAlrwI6DAZDZD'
verify_token = '8510865767'



def yt_grabber(vid):
    grabber_url = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video=http://www.youtube.com/watch?v=' + vid
    r = requests.get(grabber_url)
    return json.loads(r.text)['link']

def post_msg(fbid, data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'% access_token
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"file", "payload":{"url":data}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def search(fbid, text):
    q = text.split()
    url_q = '+'.join(q)
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=' + url_q + '&key=' + youtube_api_key
    
    #post_msg(fbid, url)
    
    r = requests.get(url)
    raw_data = r.text
    #print raw_data
    data = json.loads(raw_data)
    try:
        vid = data['items'][0]['id']['videoId']
        #print vid
        flink = 'http://www.youtubeinmp3.com/fetch/?video=https://www.youtube.com/watch?v=' + vid
        #link = yt_grabber(vid)
        post_msg(fbid, flink)
    except:
        print "No video id!"
    


class youtubebot(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == verify_token:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
 
 
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']: 
                if 'message' in message: 
                    try:
                        search(message['sender']['id'], message['message']['text'])  
                        #post_msg(message['sender']['id'], "Holla!")
                        #get_meaning(message['sender']['id'], message['message']['text'])
                        #send_yo()
                    except Exception as e:
                        print e
                        post_msg(message['sender']['id'], "Dunno!")
                        #get_meaning(message['sender']['id'], 'Please send a valid text.')    
                        #send_yo()
        return HttpResponse()