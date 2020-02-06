
import datetime
import os,sys
#import numpy as np
import requests
import boto3
#from pip._internal import main

from datetime import datetime

s3client = boto3.client('s3')

def get_files_noaa(leading_folder, bucket_name,limit, increment,degrees):
    now = datetime.utcnow()     ### current time
    print("now =", now)       
    currenttime_string = now.strftime("%m/%d/%Y %H:%M:%S")  ## string format
    currmo=currenttime_string[0:2]   ##month
    currda=currenttime_string[3:5]   ##day
    curryr=currenttime_string[6:10]  ##yr
    currhr=currenttime_string[11:13] ##hour
    currmin=currenttime_string[14:16] ##minutes
    currsec=currenttime_string[17:19] ##seconds

    FCST_IH=6 ## IH=Interval Hour
    hour = int(((int(currhr)-4)/FCST_IH)) * FCST_IH
    last_IH = int(hour)
    #last_IH= int(np.floor((int(currhr)-4)/FCST_IH) * FCST_IH) #subtracting 4 hours... time to post GFS forecast
    if last_IH<10:
        last_IH_str='0'+str(last_IH)
    else:
        last_IH_str=str(last_IH)

    ## strings for date identification
    mo_str=currmo
    da_str=currda
    hr_str=last_IH_str
    yr_str=curryr

    yrmo_str = yr_str + mo_str
    yrmoda_str = yr_str + mo_str + da_str
    yrmodahr_str = yr_str + mo_str + da_str + hr_str

    file='gfs.t'+hr_str+'z.pgrb2.1p00.f000' ## the f000 here is the forecast hour... 0:384
    filehour = 'gfs.t'+hr_str+'z.pgrb2.1p00.f'
    starfile='gfs.t'+hr_str+'z.pgrb2.1p00.f*'
    newfile=yrmodahr_str+file
    os.system('rm '+file) ## if the weather data file is already in this location, delete it
    os.system('rm '+newfile) ## if the RENAMED file already exists, delete it

    filename = 'gfs.' + yr_str+mo_str+da_str + '/' + hr_str + '/'

    #####################
    WXpath='https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.'+yr_str+mo_str+da_str+'/'+hr_str+'/'
    print(WXpath)
    
    #xx=os.system('wget '+WXpath+file) ## wget command
  

    temporaryfile = leading_folder+file
    newfile=yrmodahr_str+file
    print("newfilename:" + newfile)
    print("temporaryfile:" + leading_folder+file)
    print("bucket: " + bucket_name )
    # upload to S3
    #if bucket_name != "":
    #    s3client.upload_file(temporaryfile, bucket_name, newfile)

    timeloop = 0
    keeplooping = True
    while (keeplooping):
        timestr = str(timeloop)
        timestring = "{:03d}".format(timeloop)
        print(timestring)
        filehour = 'gfs.t'+hr_str+'z.pgrb2.' + degrees + '.f' + timestring
        response = requests.request("GET", WXpath+filehour, data="", headers="")

        print(leading_folder)
        with open(leading_folder+file, 'wb') as f:
            f.write(response.content)

        temporaryfile = leading_folder+file
        newfile=yrmodahr_str+filehour
        print(newfile)    
        print("newfilename:" + newfile)
        print("temporaryfile:" + leading_folder+file)
        print("bucket: " + bucket_name )
        if bucket_name != "":
            s3client.upload_file(temporaryfile, bucket_name, newfile)
        else:
            os.system('mv '+file+' '+newfile)  ##rename to include date

        timeloop = timeloop + int(increment)
        if timeloop > int(limit):
            keeplooping = False



def lambda_handler(event, context):

    bucket_name = os.getenv('BUCKET')
    limit = os.getenv('LIMIT')
    increment = os.getenv('INCREMENT')    
    degrees = os.getenv('DEGREES')
    leading_folder = "/tmp/"
    get_files_noaa(leading_folder, bucket_name, limit, increment,degrees)


if __name__ == '__main__': 
    bucket_name = ""
    leading_folder = ""
    limit = 384
    increment = 3
    degrees = "1P00"
    get_files_noaa(leading_folder, bucket_name, limit, increment,degrees)

