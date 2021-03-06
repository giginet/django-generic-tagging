django-generic-tagging
=========================

.. image:: https://travis-ci.org/giginet/django-generic-tagging.svg?branch=master
    :target: https://travis-ci.org/giginet/django-generic-tagging

.. image:: https://coveralls.io/repos/github/giginet/django-generic-tagging/badge.svg?branch=master
    :target: https://coveralls.io/github/giginet/django-generic-tagging?branch=master
    
.. image:: https://img.shields.io/pypi/status/django-generic-tagging.svg 
    :target: https://pypi.python.org/pypi/django-generic-tagging

.. image:: https://img.shields.io/pypi/pyversions/django-generic-tagging.svg 
    :target: https://pypi.python.org/pypi/django-generic-tagging

.. image:: https://img.shields.io/pypi/l/django-generic-tagging.svg 
    :target: https://github.com/giginet/django-generic-tagging/blob/master/LICENSE.md

Author
    giginet <giginet.net@gmail.com>
Supported python versions
    3.3, 3.4, 3.5
Supported django versions
    Django 1.7 - 1.9

A generic tagging library which enables to attach tags for every objects.

Sample Application
--------------------------

https://django-generic-tagging.herokuapp.com/

Installation
------------
Use pip_ like::

    $ pip install django-generic-tagging

.. _pip:  https://pypi.python.org/pypi/pip

Requirements
---------------------

- djangorestframework_
- jQuery 1.x / 2.x

.. _djangorestframework: http://www.django-rest-framework.org/

Usage
--------------

You should refer the example application for detail.

Configuration
~~~~~~~~~~~~~~~~~

1. Put ``generic_tagging`` into your ``INSTALLED_APPS`` at settings module

    .. code:: python

          INSTALLED_APPS = (
             ...
             'generic_tagging',
          )

2. Add URL patterns into your `urls.py`

    .. code:: python

           from django.conf.urls import include, url
           from django.contrib import admin

           from generic_tagging.api.routers import TaggingAPIRouter

           tagging_router = TaggingAPIRouter(trailing_slash=True)

           urlpatterns = [
               ...
               url(r'^tags/', include('generic_tagging.urls')),
               url(r'^api/', include(tagging_router.urls)),
           ]

3. Create ``generic_tagging`` database tables by running::

      $ python manage.py migrate


How to add tagging feature to your model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All you have to do is embed the two template tags into your models' templates.

1. Add ``{% load tagging %}`` to load tagging module

2. Place ``{% render_generic_tagging_head_tag %}`` into ``<HEAD>`` tag

3. Place ``{% render_generic_tagging_component_tag_for object %}`` to where you like.

    .. code:: html

           {% load tagging %}
           <!DOCTYPE html>
           <html lang="en">
           <head>
               <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
               {% render_generic_tagging_head_tag %}
               ...
           </head>
           <body>
               <h1>{{ object.title }}</h1>
               {% render_generic_tagging_component_tag_for object %}
           </body>
           </html>

Views
-----------------

.. table:: This library has two default views.

   ===========   ==========================================    ============================
   Description   Template path                                 Reversed URL name
   ===========   ==========================================    ============================
   Tag list      /templates/generic_tagging/tag_list.html      generic_tagging_tag_list
   Tag detail    /templates/generic_tagging/tag_detail.html    generic_tagging_tag_detail
   ===========   ==========================================    ============================


Tag list
~~~~~~~~~~~~~

This view displays all tags.

``templates/generic_tagging/tag_list.html`` should be used as the template.

    .. code:: html

            <h1>All available tags</h1>
            <ul>
                {% for tag in object_list %}
                    <li><a href="{{ tag.get_absolute_url %}">{{ tag.label }}</a></li>
                {% endfor %}
            </ul>


Tag detail
~~~~~~~~~~~~~~

Each tags have permalinks to display all related objects.

``templates/generic_tagging/tag_detail.html`` should be used as the template.

    .. code:: html

            <h1>All contents relative with {{ object.label }}</h1>
            <ul>
                {% for item in object.items.all %}
                    <li><a href="{{ item.content_object.get_absolute_url %}">{{ item.content_object }}</a></li>
                {% endfor %}
            </ul>




API
------------------

``django-generic-tagging`` has REST-ful APIs.

.. table:: List of API endpoints.

    =========================  ========== ======================
    Endpoint                   Method     Reversed URL name
    =========================  ========== ======================
    /tag/                      GET        ``tag-list``
    /tagged_item/              GET        ``tagged_item-list``
    /tagged_item/<pk>/         GET        ``tagged_item-detail``
    /tagged_item/              CREATE     ``tagged_item-list``
    /tagged_item/<pk>/         DELETE     ``tagged_item-detail``
    /tagged_item/<pk>/lock/    PATCH      ``tagged_item-lock``
    /tagged_item/<pk>/unlock/  PATCH      ``tagged_item-unlock``
    =========================  ========== ======================

License
------------------------

The MIT License (MIT)

Copyright (c) 2016 giginet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
