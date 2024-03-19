from collections import namedtuple

ListItem = namedtuple(
    "ListItem",
    ["listId", "title", "ItemIds"],
)

Item = namedtuple("Item", ["itemId", "title"])
CheckItem = namedtuple("CheckItem", ["itemId", "title", "isChecked"])
