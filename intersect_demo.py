import argparse
import os
import sys
from random import randint
import datetime
import numpy as np
import imutils
import math
import cv2
import sqlalchemy as db
import logging
import config

from linecrossingdetector import Line, LineCrossTest, MaskObj

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Logging
logging.basicConfig(level=config.LOGGING_LEVEL,format='%(asctime)s - %(message)s')
logging.info("Started Line Crossing Script")
logging.info("Logging Level : " + str(config.LOGGING_LEVEL))
logging.debug("Config Loaded")
logging.debug("DB_PATH = " + str(config.DB_DETAILS))

# Get id of the video to be processed.
try:
    args = sys.argv
    vid_id = args[1]
    line_p1 = args[2] # Line Point 1
    line_p2 = args[3] # Line Point 2
    logging.info("Parse Successfull")
except Exception as e:
    logging.error("Could not parse given data. Gracefully exiting...")
    sys.exit(500)

line_cross = Line(line_p1, line_p2)
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
    engine = create_engine(DB_PATH, echo=True)
else:
    engine = create_engine('sqlite:///anomaly.db', echo=True)
Base = declarative_base()

# DB Connection Create
# ---------------------------------------------------------
Base.metadata.create_all(engine)
connection = engine.connect()
metadata = db.MetaData()


# Tables
# ---------------------------------------------------------
anomalies_table = db.Table('DetectedAnomalies', metadata, autoload=True, autoload_with=engine)
video_table = db.Table('Videos',metadata,autoload=True, autoload_with=engine)
video_detected_objects_table = db.Table('VideoDetectedObject',metadata,autoload=True, autoload_with=engine)
detected_objs_table = db.Table('DetectedObjects', metadata, autoload=True, autoload_with=engine)


# Important part in general we grab video details here
# ---------------------------------------------------------
video_details = connection.execute(db.select([video_table]).where(video_table._columns.VideoId == vid_id)).fetchmany(1)[0]
vid_name = video_details['Name']

width = video_details['Width'] 
height = video_details['Height']


test_engine = LineCrossTest(line_cross)

detected_objs_details = []
detected_obj_video = connection.execute(db.select([video_detected_objects_table]).where(video_detected_objects_table._columns.VideoId == vid_id)).fetchall()
for item in detected_obj_video:
    details = connection.execute(db.select([detected_objs_table]).where(detected_objs_table._columns.DetectedObjectId == item['DetectedObjectId'])).fetchall()
    detected_objs_details.append(details[0])

logging.info("Processing " + vid_name)
    
mask_objs = []

for item in detected_objs_details:
    # TODO Change the coords to appropriate format
    center_x, center_y, width, height = item['']
    # TODO Variables to be fixed
    ob_d = MaskObj(center_x,center_y,width,height)
    logging.warning("Trying Masking Operation")
    mask_objs.append(ob_d)
    res = test_engine.getMaskingResult(ob_d)
    logging.info("Masking Operation Successful with result" + str(res))
    if res:
        connection.execute(insert(anomalies).values(detected_anomaly = "Line Crossing Detected", frame_id=item['FrameNo'], center_x = ob_d.get_x(), center_y = ob_d.get_y(), width = ob_d.width(), height = ob_d.get_height()) )




