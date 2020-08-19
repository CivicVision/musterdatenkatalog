from django import template
from django.urls import reverse
import re

register = template.Library()

MAIN_MENUE = [
        { 'name': 'musterdaten:index', 'title': "Start", 'page_title': "Musterdatenkatalog" },
        { 'name': 'musterdaten:ueber', 'title': "Über" },
        ]

def create_menu(menu_item, request):
    url = reverse(menu_item.get('name'))
    menu_item['link'] = url
    menu_item['class'] = active_menu_item(request.path, url)
    return menu_item

@register.inclusion_tag('menu.html', takes_context=True)
def show_main_menu(context, classes):
    request = context['request']
    menu = [create_menu(item, request) for item in MAIN_MENUE]
    return {'classes': classes, 'main': menu }

@register.simple_tag
def main_title(request):
    for menu_item in MAIN_MENUE:
        if request.path == reverse(menu_item.get('name')):
            return menu_item.get('page_title', menu_item.get('title'))
    return ''

@register.simple_tag
def active_menu_item(path, url):
    if url == path:
        return 'text-white bg-gray-900'
    return 'text-gray-300'
