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

class NluAPISample:
    API_NAME_SEG = "seg";
    API_NAME_NLI = "nli";
    
    apiBaseUrl = ''
    appKey = ''
    appSecret = ''
    
    def __init__(self):
        pass
    
    
    def setAuthorization(self, appKey, appSecret):
        self.appKey = appKey
        self.appSecret = appSecret
        
    
    '''Setup localization to select service area, this is related to different 
       server URLs or languages, etc.
     
       :param language the language type.'''
    def setLocalization(self, apiBaseURL):
        self.apiBaseUrl = apiBaseURL
    
    '''Get the NLU recognition result for your input text.
     
      :param inputText the text you want to recognize.'''
    def getRecognitionResult(self, apiName, inputText):
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
        rq = '{\"data_type\":\"stt\",\"data\":{\"input_type\":1,\"text\":\"'+inputText+'\"}}'
        postData = 'appkey='+str(self.appKey)
        postData +='&api='+apiName
        postData +='&timestamp='+str(timestamp)
        postData +='&sign='+str(sign)
        postData +='&rq='
        
        if (apiName == self.API_NAME_SEG):
            postData += inputText
        elif(apiName == self.API_NAME_NLI):           
            postData += rq
        
        '''Request NLU service by HTTP POST'''
        req = urllib.request.Request(self.apiBaseUrl,postData.encode("utf-8"))
        with urllib.request.urlopen(req) as f:
            getResponse = f.read().decode('utf-8')
        
        
        '''Now you can check the status here.'''
        print("Sending 'POST' request to URL : " + self.apiBaseUrl)
        print("Post parameters : " + str(postData))
        print("Response Code : " + str(f.getcode()))
        
        '''Get the response'''
        return str(getResponse)