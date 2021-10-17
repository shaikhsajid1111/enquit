from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import json

def fetch_posts(request):
  return JsonResponse({"name":"sajid"},content_type="application/json",safe=False)

