import logging
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk # type: ignore
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import json
from plumbum import local

logger = logging.getLogger(__name__)
hyprctl = local["hyprctl"]

class ItemEnterEventListener(EventListener):
  def on_event(self, event, extension):
    data = event.get_data()
    hyprctl(["dispatch", "focuswindow", "address:{}".format(data["address"])])

class DemoExtension(Extension):
  def __init__(self):
    super().__init__()
    self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
    self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
  def on_event(self, event, extension):
    icon_theme = Gtk.IconTheme.get_default()

    items = []
    windows = json.loads(hyprctl(["clients", "-j"]))
    for i in windows: # type: ignore
      if len(i["title"]) > 0:
        icon = 'images/icon.png'
        icon_info = icon_theme.lookup_icon(i["class"], 48, 0)
        if icon_info is not None:
          icon = icon_info.get_filename()
        data = { 'address': i['address'] }
        items.append(ExtensionResultItem(icon=icon,
                                         name=i["title"],
                                         on_enter=ExtensionCustomAction(data, keep_app_open=False)))

    return RenderResultListAction(items)

if __name__ == '__main__':
  DemoExtension().run()
