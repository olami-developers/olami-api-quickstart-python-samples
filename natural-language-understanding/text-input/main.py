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

from nluapi import NluAPISample
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str,
                    help="server base URL according to servicing area")
    parser.add_argument("appKey", type=str,
                    help="your app key which get from server of servicing area")
    parser.add_argument("appSecret", type=str,
                    help="your app secret which get from server of servicing area")
    parser.add_argument("inputText", type=str,
                    help="input text which you want to talk with olami")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
    args = parser.parse_args()
    
    nluApi = NluAPISample()
    nluApi.setLocalization(args.url)
    nluApi.setAuthorization(args.appKey, args.appSecret)     
    
    print("\n---------- Test NLU API, api=seg ----------\n");
    print("\nResult:\n\n", nluApi.getRecognitionResult(nluApi.API_NAME_SEG, args.inputText))
    
    print("\n---------- Test NLU API, api=nli ----------\n");
    print("\nResult:\n\n", nluApi.getRecognitionResult(nluApi.API_NAME_NLI, args.inputText))


if __name__ == '__main__':
    main()