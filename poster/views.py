import random
import openai
import json
from django.shortcuts import redirect, render
import requests

from poster.models import events

# Create your views here.
pexels_api = "563492ad6f91700001000001fcb263fc16bb46568145486eadb0f08e"
# open_ai_api = "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"


openai.api_key = 'API KEY'


url = "Authorization: 563492ad6f91700001000001fcb263fc16bb46568145486eadb0f08e" \
    "https://api.pexels.com/v1/search?query=people"


def index(request):

    # print(json.dumps(response.json()))

    if request.method == "POST":
        event = request.POST['name']
        date = request.POST['date']
        time = request.POST['time']
        about = request.POST['about']
        tags = request.POST['tags']
        info = request.POST['info']

        print(event, date, time, about, tags)

        data = events.objects.create(
            event_name=event,
            event_on_date=date,
            event_on_time=time,
            about_event=about,
            tags=tags,
            additional_info=info
        )
        data.save()
        return redirect("/")

    fetch_data = events.objects.all()
    context = {"data": fetch_data}

    return render(request, "index.html", context)


def poster(requset, id):
    fetch_data = events.objects.filter(id=id)
    print(fetch_data[0])
    headers = {
        'Authorization': '563492ad6f91700001000001fcb263fc16bb46568145486eadb0f08e', }
    params = {'query': fetch_data[0].tags,
              'per_page': '5', 'orientation': 'square'}
    response_img = requests.get(
        'https://api.pexels.com/v1/search', params=params, headers=headers)

    img = response_img.json()['photos'][random.randint(0, 4)]["src"]["large"]
    
    # response_heading = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=f"write a catchy poster heading for event name : {fetch_data[0].event_name} and event about : {fetch_data[0].about_event}",
    #     temperature=0.8,
    #     max_tokens=80,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    # )


    context = {
        "data": fetch_data,
        "image": img,
        # "image" : "https://images.pexels.com/photos/14103314/pexels-photo-14103314.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "tags": fetch_data[0].tags,
        # "heading": response_heading['choices'][0]['text']
        "heading" : "Looking To Build A Business That Generates Passive Income? Look No Further! Our Network Marketing Event Will Teach You Everything You Need To Know!"
    }

    return render(requset, "poster.html", context)


def poster_delete(requset, id):
    fetch_data = events.objects.filter(id=id)
    fetch_data.delete()
    return redirect("/")
