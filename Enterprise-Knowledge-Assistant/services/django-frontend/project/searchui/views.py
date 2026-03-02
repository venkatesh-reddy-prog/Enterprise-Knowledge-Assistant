import requests
from django.shortcuts import render

FASTAPI_URL = "http://localhost:8300/query"

def home(request):
    response_text = None

    if request.method == "POST":
        query = request.POST.get("query")
        try:
            res = requests.post(FASTAPI_URL, json={"query": query})
            response_text = res.json().get("answer", "No response")
        except Exception as e:
            response_text = f"Error: {str(e)}"

    return render(request, "searchui/home.html", {"response": response_text})