import pluggy

from . import hookspecs


pm = pluggy.PluginManager("django_simple_deploy")
pm.add_hookspecs(hookspecs)
