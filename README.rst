=======
Hoarder
=======

The ultimate analytics kit for Django.

Hoarder in an event tracking API for Django that supports multiple analytics backends: KISSMetrics, Google Analytics, local MongoDB. 

Hoarder is for you if:

- You want to use multiple web analytics tools without duplicating code for each of them
- You want to be able to swap analytics packages without changing your code
- You want to have a local copy of all your analytics data

------------
Installation
------------
1. Run `pip install hoarder`
2. Add `'hoarder'` app to `INSTALLED_APPS` 
3. Add `'hoarder.middleware.LoggingMiddleware'` and `'hoarder.middleware.DeduplicationMiddleware'` to `MIDDLEWARE_CLASSES`
4. Add the following to the beginning of head section in your base template:
   ::

      {% load hoarder_tags %}
      {% tracking_code %}

5. Specify the backends you want to use in `HOARDER_BACKENDS` settings variable

------------------
Supported backends
------------------
- `hoarder.backends.LogBackend` - just outputs all events to log for debug purposes
- `hoarder.mongo.MongoBackend` - stores all events in a local MongoDB database
- `hoarder.backends.KISSMetricsBackend` - sends all events to KISSMetrics 

--------
Settings
--------

`HOARDER_BACKENDS` - list of enabled backends

`HOARDER_MONGO_DATABASE` - for Mongo backend, name of the database to use

`KISSMETRICS_API_KEY` - for KISSMetrics backend, the API key from your KISSMetrics account

-----
Usage
-----

Registering an event in view::

 from hoarder import register_request_event
 ...
 register_request_event(request, 'signed up', {'plan level' : 'Basic'})

Registering an event outside of a view::

 from hoarder import register_request_event
 ...
 register_user_event(user, 'billed', {'amount' : '49.99'})

Labeling current visitor::

 from hoarder import label_visitor, 
 ...
 label_visitor(request, 'Nice person')

