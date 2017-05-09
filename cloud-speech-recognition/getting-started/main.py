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

from asrapi import SpeechAPISample
import argparse
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str,
                    help="server base URL according to servicing area")
    parser.add_argument("appKey", type=str,
                    help="your app key which get from server of servicing area")
    parser.add_argument("appSecret", type=str,
                    help="your app secret which get from server of servicing area")
    parser.add_argument("audioFilePath", type=str,
                    help="the audio file you want to upload")
    parser.add_argument("compressFlag", type=int, default=0,choices=[0,1],
                    help="set 1 if the audio file is a Speex audio")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
    args = parser.parse_args()
    
    compressed = True if args.compressFlag is "1" else False
    
    asrApi = SpeechAPISample()
    asrApi.setLocalization(args.url)
    asrApi.setAuthorization(args.appKey, args.appSecret)     
    
    '''Start sending audio file for recognition'''
    print("\n----- Test Speech API, seq=nli,seg -----\n")
    print("\nSend audio file... \n");
    responseString =  asrApi.sendAudioFile(asrApi.API_NAME_ASR, 
            "nli,seg", True, args.audioFilePath, compressed)
    print("\n\nResult:\n\n" , responseString, "\n")
    
    ''' Try to get recognition result if uploaded successfully.    
        We just check the state by a lazy way :P , you should do it by JSON.'''
    if ("error" not in responseString.lower()): 
        print("\n----- Get Recognition Result -----\n")
        time.sleep(1) #delay for 1 second
        ''' Try to get result until the end of the recognition is complete '''
        while (True):
            responseString = asrApi.getRecognitionResult(
                    asrApi.API_NAME_ASR, "nli,seg")
            print("\n\nResult:\n\n" , responseString ,"\n")
            ''' Well, check by lazy way...again :P , do it by JSON please. '''
            if ("\"final\":true" not in responseString.lower()): 
                print("The recognition is not yet complete.")
                if ("error" in responseString.lower()): 
                    break
                time.sleep(2) #delay for 2 second
            else: 
                break
    
    print("\n\n")


if __name__ == '__main__':
    main()