from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os
from data_processing.graph_maker_v2 import graph_maker_function, allowed_data, allowed_data_stripped
import time

current_dir = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
template_test_view_dir = current_dir
template_test_view_dir = os.path.join(template_test_view_dir, "templates")
template_test_view_dir = os.path.join(template_test_view_dir, "test_view")




def index(request):
    return render(request, os.path.join(template_test_view_dir,'homepage.html'),context={'data_present':allowed_data(),"fdata_present":allowed_data_stripped()})

def citation_render(request):
    return render(request, os.path.join(template_test_view_dir,'citations.html'))

def handling_404(request, exception):
    return render(request, os.path.join(template_test_view_dir, '404.html'))

def handling_500(request):
    return render(request, os.path.join(template_test_view_dir, '404.html'))

# def graph_gen(request, id):
#     graph_file_path = os.path.join('main_view/templates/test_view', f'{id}.html')
#     if os.path.exists(graph_file_path):
#         if ( (time.time()) - (os.path.getctime(graph_file_path)) ) > 86400:
#             os.remove(graph_file_path)
#             graph_maker_function(id)
#         return render(request, f"test_view/{id}.html")
#     else:
#         graph_maker_function(id)
#         return render(request, f"test_view/{id}.html")


def graph_gen(request, id):
    graph_file_path = os.path.join(template_test_view_dir, f'{id}.html')

    graph_maker_function(id)

    response = render(request, f"test_view/{id}.html")

    if os.path.exists(graph_file_path):
        os.remove(graph_file_path)

    return response