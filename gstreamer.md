# xavior gstreamer 

* sudo apt-get install v4l-utils 

* sudo v4l2-

--- 

*  sometimes '!' separates options from CAPS --
     each CAP has COMMA separation....
	 
*  sometimes '!' is for next item in chain of modules
  
*  gst-launch-1.0 audiotestsrc ! alsasink 
  
*  -- results in tone going to speaker

*  gst-inspect-1.0 audiotestsrc 
  
*  goes from SINK to provide a SOURCE ** SEEMS TOTALLY BACKWARDS **
  look at PADS -- 'src' has no input pad, only an OUTPUT pad 
  PROPERTIES can be SET -- ex: wave=3 (triangle wave) freq=1000
  gst-launch-1.0 audiotestsrc wave=3 freq=900 volume=0.75 ! alsasink
  
   
* gst-inspect-1.0 alsasink
  --- look at capabilities 'audio/x-raw' and format='U8' for instance
  gst-launch-1.0 audiotestsrc wave=3 freq=900 volume=0.75 ! audio/x-raw,format=U8 ! alsasink

---
* gst-launch-1.0 videotestsrc ! ximagesink
* gst-inspect ximagesink
  look at video 'sink' capabilties -- 'video/x-raw'
  can also use videoconvert (software convertor)
  


* gst-launch-1.0 videotestsrc ! autovideoconvert ! ximagesink

* CSI camera  -- use nvarguscamerasrc 


---

* videoconvert ! video/x-raw, format=BGR ! appsink

* 'v4l2src device=/dev/video2 ! video/x-raw,width='+str(width)+',height='+str(height)+'  etc
