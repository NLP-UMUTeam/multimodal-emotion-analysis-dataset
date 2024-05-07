"""
This script is used to obtain the first version of the dataset 
for the generation of the baselines.

What it does is to use public.csv and filters 

"""

import hashlib
import glob
import moviepy.editor as mp
import numpy as np
import os
import pandas as pd
import sys

from pydub import AudioSegment
from pytube import YouTube
from tqdm import tqdm

def main ():

    # @var paths Dict
    paths = {
        'input': os.path.join ('..', 'output', 'dataset.csv'),
        'output': os.path.join ('..', 'output', 'dataset_v1')
    }
    
    
    # Add inner paths
    paths['output_video'] = os.path.join (paths['output'], 'videos')
    paths['output_audios'] = os.path.join (paths['output'], 'segments')
    
    
    # @var df Pandas Dataframe
    df = pd.read_csv (paths['input'])
    
    
    # @var pbar TQDM
    pbar = tqdm (df.iterrows (), total = len (df))
    
    
    # @var videos_that_cant_be_downloded List
    videos_that_cant_be_downloded = []
    
    
    for index, row in pbar:
        
        # Indicate name
        pbar.set_description (row['filename'])
        
        
        # Step 1. Download video
        # @var video_path String
        video_path = os.path.join (paths['output_video'], row['youtube_key'] + '.mp4')


        # @var video_already_downloaded boolean
        video_already_downloaded = False
        
    
        # Skip those videos that already has a video
        # and the size of the video is not 0
        if os.path.isfile (video_path):
            if os.stat (video_path).st_size != 0:
                video_already_downloaded = True
        
        # Download video
        if not video_already_downloaded:
            try:
                # @var video  Youtube Video
                video = YouTube ('https://www.youtube.com/watch?v=' + row['youtube_key'])
                video = video.streams.get_highest_resolution ()
                video.download (output_path = paths['output_video'], filename = row['youtube_key'] + '.mp4')
            
            except Exception as e:
                videos_that_cant_be_downloded.append (row['youtube_key'])
                print (row['youtube_key'] + " can't be downloaded")
                print (e)
                continue
        
        
        # Step 2: Get audio
        # @var audio_path String
        audio_path = os.path.join (paths['output_audios'], row['filename'])


        # @var segment_already_downloaded boolean
        segment_already_downloaded = False


        # Skip those videos that already has an audio
        # and the size of the audio is not 0
        if os.path.isfile (audio_path):
            if os.stat (audio_path).st_size != 0:
                segment_already_downloaded = True

        force_download = []
        
        if row['youtube_key'] in force_download:
            segment_already_downloaded = False


        # Download segment
        if not segment_already_downloaded:

            # @var start_time float
            start_time = int (row['start_time']) / 1000
            
            
            # @var end_time float
            end_time = int (row['end_time']) / 1000

            
            try:
                
                # @var clip
                clip = mp.VideoFileClip (video_path)


                
                # @var audio AudioSegment
                audio = clip.subclip (start_time, end_time).audio.write_audiofile (audio_path, verbose = False, logger = None)
            
            except Exception as e:
                print (e)
                print (row['youtube_key'] + " can't be encoded as audio")
                continue
            
            
    print ("Videos that cannot be loaded")
    print (videos_that_cant_be_downloded)
        

if __name__ == "__main__":
    main ()