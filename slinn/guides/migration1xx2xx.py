migration1xx2xx = """How to migrate from 1xx(1.2.1) to 2xx(2.0.0-2.2.4)

Firstly, change all your @dp_xxx.route(...) to @dp_xxx(...)
Then, you should change some filters from Filter to AnyFilter or LinkFilter where it is suit
If you have troubles with Smart Navigation, then specify '{"smart_navigation": false}' in your project.json

If you want support of autoreloading your app, follow these steps:
- Change dp_xxx = Dispatcher(...) to dp = Dispatcher(...) and @dp_xxx.route(...) to @dp(...) OR dp = dp_xxx in the end of the file
- Execute `py manage.py migrate_app {app`s name}`
"""