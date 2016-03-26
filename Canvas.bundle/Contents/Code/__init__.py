import re, string, json
from collections import OrderedDict

CANVAS_URL = 'http://www.canvas.be/api/program/a2z'
CANVAS_PROGRAM_URL = 'http://www.canvas.be/api/video/1/0,999999/-date/_p%d'

ICON = 'CANVAS_logo_zwart.jpg'

RE_JSON = Regex("programEpisodes = (.*);")

####################################################################################################
def Start():

    ObjectContainer.title1 = 'Canvas'
    DirectoryObject.thumb = R(ICON)
    VideoClipObject.thumb = R(ICON)
    HTTP.CacheTime = 1800

####################################################################################################
@handler('/video/canvas', 'Canvas')
def MainMenu():

    oc = ObjectContainer()
  
    # Request the json
    json = JSON.ObjectFromURL(CANVAS_URL)
    
    for program in json['data']:

        # Skip programs that are not available online
        if program['isVideoZoneUrl']:
            
            Log.Info(program)
            
            title = program['title']
            description = program['timeIndication']
            url = program['url']
            pid = program['id']
            thumb = program['image']['data']['url']

            oc.add(DirectoryObject(
                key = Callback(GetItemList, title=title, url=url, pid=pid),
                title = title,
                summary = description,
                thumb = thumb
            ))

    return oc

####################################################################################################

def GetItemList(url, title, pid):

    oc = ObjectContainer(title1=title)

    Log.Info(url)

    # Request the json
    json = JSON.ObjectFromURL(CANVAS_PROGRAM_URL % pid)
    
    #request = HTTP.Request(CANVAS_PROGRAM_URL % pid)
    #json_ordered = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(request)
    Log.Info(json)
    
    for key in json['videos']:

        video_page_url = json['videos'][key]['link']
        show_title = json['videos'][key]['title']
        description = json['videos'][key]['description']
        thumb = json['videos'][key]['image']['url']
        originally_available_at = Datetime.ParseDate(json['videos'][key]['date']['date'])
        
        if json['videos'][key]['length']:
            duration = int(float(json['videos'][key]['length']) * 1000)
            
        Log.Info(show_title)

        oc.add(
            VideoClipObject(
                url = video_page_url,
                title = show_title,
                summary = description,
                thumb = thumb,
                originally_available_at = originally_available_at,
                duration = duration
            )
        )
        
    return oc