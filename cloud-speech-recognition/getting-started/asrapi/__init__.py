#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Copyright 2017, VIA Technologies, Inc. & OLAMI Team.
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''
import time
import hashlib
import urllib.request, urllib.error

class SpeechAPISample:
    API_NAME_ASR = "asr";
    
    apiBaseUrl = ''
    appKey = ''
    appSecret = ''
    cookies = ''
    
    def __init__(self):
        pass
    
    '''Setup your authorization information to access OLAMI services.

        :param appKey the AppKey you got from OLAMI developer console.
        :param appSecret the AppSecret you from OLAMI developer console. '''
    def setAuthorization(self, appKey, appSecret):
        self.appKey = appKey
        self.appSecret = appSecret

    
    '''Setup localization to select service area, this is related to different 
       server URLs or languages, etc.
     
       :param apiBaseURL URL of the API service.'''
    def setLocalization(self, apiBaseURL):
        self.apiBaseUrl = apiBaseURL

    
    '''Send an audio file to speech recognition service.
     
      :param apiName the API name for 'api=xxx' HTTP parameter.
      :param seqValue the value of 'seq' for 'seq=xxx' HTTP parameter.
      :param finished TRUE to finish upload or FALSE to continue upload.
      :param filePath the path of the audio file you want to upload.
      :param compressed TRUE if the audio file is a Speex audio.'''    
    def sendAudioFile(self, apiName, seqValue, finished, filePath, compressed): 
        '''Read the input audio file'''
        with open(filePath, "rb") as audioFile:
            af = audioFile.read()
            bAudioData = bytearray(af)
        if (bAudioData is None): 
            return "[ERROR] File not found!";
        
        ''' composite post data field''' 
        postData = str(self.getBasicQueryString(apiName, seqValue))
        postData += "&compress=" + ("1" if compressed else "0")
        postData += "&stop=" + ("1" if finished else "0")
        
        ''' Request speech recognition service by HTTP POST '''
        url = str(self.apiBaseUrl) + "?" + str(postData)
        headers = { 'Connection'    : "Keep-Alive",
                    'Content-Type'  : "application/octet-stream" }
        req = urllib.request.Request(url,bAudioData,headers)
        with urllib.request.urlopen(req) as f:
            getResponse = f.read().decode()
        
        '''Now you can check the status here.'''
        print("Sending 'POST' request to URL : " + self.apiBaseUrl)
        print("Post parameters : " + str(postData))
        print("Response Code : " + str(f.getcode()))
        
        '''Get cookie'''
        self.cookies = f.getheader('Set-Cookie')
        if (self.cookies is None): 
            return "Failed to get cookies.";
        print("Cookies : " + str(self.cookies))
        
        '''Get the response'''
        return str(getResponse)


    ''' Get the speech recognition result for the audio you sent.
    
        :param apiName the API name for 'api=xxx' HTTP parameter.
        :param seqValue the value of 'seq' for 'seq=xxx' HTTP parameter. '''    
    def getRecognitionResult(self, apiName, seqValue):
        query = self.getBasicQueryString(apiName, seqValue) + "&stop=1"

        '''Request speech recognition service by HTTP GET'''
        url = str(self.apiBaseUrl) + "?" + str(query)
        req = urllib.request.Request(url,headers = {'Cookie': self.cookies})
        with urllib.request.urlopen(req) as f:
            getResponse = f.read().decode()
        
        '''Now you can check the status here.'''
        print("Sending 'GET' request to URL : " + self.apiBaseUrl)
        print("get parameters : " + str(query))
        print("Response Code : " + str(f.getcode()))
        
        '''Get the response'''
        return str(getResponse)
    
    
    '''Generate and get a basic HTTP query string
     
        :param apiName the API name for 'api=xxx' HTTP parameter.
        :param seqValue the value of 'seq' for 'seq=xxx' HTTP parameter.'''
    def getBasicQueryString(self, apiName, seqValue):
        timestamp = int(round(time.time() * 1000))
        
        '''Prepare message to generate an MD5 digest.'''
        signMsg = str(self.appSecret)
        signMsg += 'api='+apiName
        signMsg += 'appkey='+str(self.appKey)
        signMsg += 'timestamp='+str(timestamp)
        signMsg += str(self.appSecret)
        
        '''Generate MD5 digest.'''
        md = hashlib.md5()
        md.update(signMsg.encode('utf-8'))
        sign = md.hexdigest()
        
        '''Assemble all the HTTP parameters you want to send'''
        postData = 'appkey='+str(self.appKey)
        postData +='&api='+apiName
        postData +='&timestamp='+str(timestamp)
        postData +='&sign='+str(sign)
        postData +='&seq=' +seqValue
        
        return str(postData)

        