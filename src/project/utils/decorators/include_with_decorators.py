"""
A replacement for ``django.conf.urls.include`` that takes a decorator,
or an iterable of view decorators as the first argument and applies them, in
reverse order, to all views in the included urlconf.
"""

from importlib import import_module

from django.urls import URLPattern, URLResolver, include
from django.utils.functional import cached_property

class DecoratedPatterns(object):
    """
    A wrapper for an urlconf that applies a decorator to all its views.
    """
    def __init__(self, urlconf_module, decorators):
        # ``urlconf_module`` may be:
        #   - an object with an ``urlpatterns`` attribute
        #   - an ``urlpatterns`` itself
        #   - the dotted Python path to a module with an ``urlpatters`` attribute
        self.urlconf = urlconf_module
        try:
            iter(decorators)
        except TypeError:
            decorators = [decorators]
        self.decorators = decorators

    def decorate_pattern(self, pattern):
        if isinstance(pattern, URLResolver):
            decorated = URLResolver(
                pattern.pattern,
                DecoratedPatterns(pattern.urlconf_module, self.decorators),
                pattern.default_kwargs,
                pattern.app_name,
                pattern.namespace,
            )
        else:
            callback = pattern.callback
            for decorator in reversed(self.decorators):
                callback = decorator(callback)
            decorated = URLPattern(
                pattern.pattern,
                callback,
                pattern.default_args,
                pattern.name,
            )
        return decorated

    @cached_property
    def urlpatterns(self):
        # urlconf_module might be a valid set of patterns, so we default to it.
        patterns = getattr(self.urlconf_module, 'urlpatterns', self.urlconf_module)
        return [self.decorate_pattern(pattern) for pattern in patterns]

    @cached_property
    def urlconf_module(self):
        if isinstance(self.urlconf, str):
            return import_module(self.urlconf)
        else:
            return self.urlconf

    @cached_property
    def app_name(self):
        return getattr(self.urlconf_module, 'app_name', None)


def decorator_include(decorators, arg, namespace=None):
    """
    Works like ``django.conf.urls.include`` but takes a view decorator
    or an iterable of view decorators as the first argument and applies them,
    in reverse order, to all views in the included urlconf.
    """
    if isinstance(arg, tuple) and len(arg) == 3 and not isinstance(arg[0], str):
        # Special case where the function is used for something like `admin.site.urls`, which
        # returns a tuple with the object containing the urls, the app name, and the namespace
        # `include` does not support this pattern (you pass directly `admin.site.urls`, without
        # using `include`) but we have to
        urlconf_module, app_name, namespace = arg
    else:
        urlconf_module, app_name, namespace = include(arg, namespace=namespace)
    return DecoratedPatterns(urlconf_module, decorators), app_name, namespace



"""
https://github.com/twidi/django-decorator-include

BSD 2-Clause License

Copyright (c) 2016, Jeff Kistler
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""