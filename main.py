#!/usr/bin/python3
from notion.client import NotionClient
import todoist
from canvasapi import Canvas
from datetime import datetime
from dateutil import parser
from dateutil import tz
import time

def getCanvasToken():
    canvas_token = ""
    try:
      temp = open("Tokens/canvas.txt", "r")
      canvas_token = temp.read().strip("\n")
    except IOError:
      print("Error: Could Not Find Canvas Token.")
    
    return canvas_token

def getNotionPage(): 
    notion_page = ""
    try:
      temp = open("Tokens/notion_page.txt", "r")
      notion_page = temp.read().strip("\n")
    except IOError:
      print("Error: Could Not Open Notion Page.")
    
    return notion_page


def getTodoistToken():
    todoist_token = ""
    try:
      temp = open("Tokens/todoist.txt", "r")
      todoist_token = temp.read().strip("\n")
    except IOError:
      print("Error: Could Not Find Todoist Token.")

    return todoist_token

def getNotionToken():
    notion_token = ""
    try:
      temp = open("Tokens/notion.txt", "r")
      notion_token = temp.read().strip("\n")
    except IOError:
      print("Error: Could Not Find Todoist Token.")

    return notion_token


def convertToUTC(date):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    temp_date = date.replace(tzinfo=from_zone)
    central = temp_date.astimezone(to_zone)
    return central

def getCanvasEvents():
    API_URL = "https://canvas.vt.edu"
    canvas = Canvas(API_URL, getCanvasToken())
    events = canvas.get_upcoming_events()

    canvas_todo = []

    for item in events:
        if 'assignment' in item:
            date = parser.parse(item['assignment']['due_at'])
            formated_date = "{}-{}-{} {}:{}:{}".format(
                date.year, date.month, date.day, date.hour, date.minute, date.second)
            formated_date = convertToUTC(date)

            title = item['title']
            canvas_todo.append([title, formated_date])

    return canvas_todo

def getNotionList(token, url): 
    client = NotionClient(token)
    page = client.get_collection_view(url)
  
    notion_todo = []
    for row in page.collection.get_rows(): 
        row_date = row.due_date 

        if row.done == True: 
          continue
        if row_date != None: 
            row_date = row_date.start
        notion_todo.append([row.task_name, row_date])
    
    return notion_todo

        

def getTodoistList(token):
    api = todoist.TodoistAPI(token)
    todoist_list = []
    items = api.state["items"]
    for item in items:
      todoist_list.append([item["content"], item["due"]['date']])
    
    return todoist_list

def main(): 
    notion_tok = getNotionToken()
    todoist_tok = getTodoistToken()
    canvas_tok = getCanvasToken() 
    notion_page = getNotionPage()

    if notion_tok != "" and todoist_tok != "" and canvas_tok != "" and notion_page != "":
        notion_list = getNotionList(notion_tok, notion_page)
        print(notion_list)
        todoist_list = getTodoistList(todoist_tok)
        print(todoist_list)
        canvas_list = getCanvasEvents()
        print(canvas_list)




        


if __name__ == '__main__': 
    main()
