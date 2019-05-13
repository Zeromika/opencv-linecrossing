import argparse
import os
import sys
import time
from random import randint
import datetime
import numpy as np
import imutils
import math
import cv2
import sqlalchemy as db
import logging
import config
import json
from math import ceil

from linecrossingdetector import Line, LineCrossTest, MaskObj

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

def info_function(value):
    sys.stdout.write(json.dumps(dict(progress=ceil(value)), indent=2))
    sys.stdout.flush()

# Logging
logging.basicConfig(filename=str(config.LOG_PATH),level=config.LOGGING_LEVEL,format='%(asctime)s - %(message)s')
logging.info("Started Line Crossing Script")
logging.info("Logging Level : " + str(config.LOGGING_LEVEL))
logging.debug("Config Loaded")
logging.debug("DB_PATH = " + str(config.DB_DETAILS))

# Get id of the video to be processed.
try:
    args = sys.argv
    vid_id = args[1]
    line_p1 = int(args[2]) # Line Point 1
    line_p2 = int(args[3]) # Line Point 2
    line_p3 = int(args[4]) # Line Point 1
    line_p4 = int(args[5]) # Line Point 2
    logging.info("Parse Successfull")
except Exception as e:
    logging.error("Could not parse given data. Gracefully exiting...")
    sys.exit(500)

line_cross = Line((line_p1, line_p2), (line_p3, line_p4))
# DB Engine Create
# --------------------------------------------------
# TODO Swap to Environment Variables
# try:
#     DB_PATH = os.environ['DB_PATH']
# except:
#     DB_PATH = None
# If config DB_PATH is set use that engine instead
logging.warning("Initiating Database Engine")
DB_PATH = config.DB_DETAILS['DB_PATH']
if DB_PATH:
    engine = create_engine(DB_PATH, echo=False)
else:
    engine = create_engine('sqlite:///anomaly.db', echo=False)
Base = declarative_base()

# DB Connection Create
# ---------------------------------------------------------
Base.metadata.create_all(engine)
connection = engine.connect()
metadata = db.MetaData()


# Tables
# ---------------------------------------------------------
anomalies_table = db.Table('detected_anomalies', metadata, autoload=True, autoload_with=engine)
video_table = db.Table('videos',metadata,autoload=True, autoload_with=engine)
detected_objs_table = db.Table('detected_objects', metadata, autoload=True, autoload_with=engine)
video_anomalies_table = db.Table('video_detected_anomaly', metadata, autoload=True, autoload_with=engine)


# Important part in general we grab video details here
# ---------------------------------------------------------
video_details = connection.execute(db.select([video_table]).where(video_table._columns.video_id == vid_id)).fetchmany(1)[0]
vid_name = video_details['name']

width = video_details['width'] 
height = video_details['height']


test_engine = LineCrossTest(line_cross, width=width, height=height)

detected_objs_details = connection.execute(db.select([detected_objs_table]).where(detected_objs_table._columns.video_id == vid_id)).fetchall()


logging.info("Processing " + vid_name)
    
mask_objs = []
processed = 0
for item in detected_objs_details:

    left_x = item['left_x']
    top_y = item['top_y']
    width = item['width']
    height = item['height']
    # Recieved Data is left_x, top_y
    center_x = left_x + width/2
    center_y = top_y - height/2
   
    ob_d = MaskObj(center_x,center_y,width,height)

    logging.warning("Trying Masking Operation")
    mask_objs.append(ob_d)
    res = test_engine.getMaskingResult(ob_d)
    logging.info("Masking Operation Successful for Frame : " + str(item['frame_no']) + " with result " + str(res))
    processed = processed + 1
    time.sleep(0.15) # Sleep half a second to process data
    info_function((processed/len(detected_objs_details)*100))
    if res:
        query = connection.execute(db.insert(anomalies_table).values(rule_id = 2,frame_no =item['frame_no'],left_x = ob_d.get_x(), top_y = ob_d.get_y(), width = ob_d.get_width(), height = ob_d.get_height()), params = json.dumps(args) )
        query2 = connection.execute(db.insert(video_anomalies_table).values(detected_anomaly_id = query.lastrowid , video_id = vid_id))

sys.exit(0)