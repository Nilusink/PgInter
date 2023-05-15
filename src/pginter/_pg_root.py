"""
_pg_root.py
04. February 2023

the root of the window

Author:
Nilusink
"""
from .widgets import GeometryManager
from .theme import ThemeManager
from copy import deepcopy
from .types import *
import typing as tp
import pygame as pg
import os.path

# for type hints
if tp.TYPE_CHECKING:
    from .widgets import Frame


DEFAULT_TITLE: str = "Window"
DEFAULT_ICON: str = os.path.dirname(__file__) + "/icon.png"


class PgRoot(GeometryManager):
    _focus_item: GeometryManager | None = None
    _running: bool = True
    _theme: ThemeManager = ...
    __background: pg.Surface = ...
    layout_params: BetterDict = ...
    _min_size: tuple[int, int] = ...
    _bg_configured: bool = False
    _mouse_pos: tuple[int, int] = ...
    _max_framerate: int = ...

    def __init__(
            self,
            title: str = ...,
            icon_path: str = ...,
            size: tuple[int, int] = ...,
            bg_color: Color = ...,
            padding: int = 0,
            margin: int = 0,
            max_framerate: int = 30
    ):
        self._max_framerate = max_framerate

        super().__init__()
        self._theme = ThemeManager()
        self._theme.notify_on(ThemeManager.NotifyEvent.theme_reload, self.notify)
        self._min_size = (0, 0)

        # args
        self._bg_configured = bg_color is not ...
        self._bg = self._theme.root.bg.hex if bg_color is ... else bg_color

        self._layout_params = BetterDict({
            "padding": padding,
            "margin": margin,
        })

        # pg init
        pg.init()
        pg.font.init()
        self._clk = pg.time.Clock()

        if size is not ...:
            self.__background = pg.display.set_mode(size, flags=pg.RESIZABLE)

        else:
            self.__background = pg.display.set_mode(flags=pg.RESIZABLE)

        # set icon and caption
        pg.display.set_caption(DEFAULT_TITLE if title is ... else title)
        img = pg.image.load(DEFAULT_ICON if icon_path is ... else icon_path, "icon")
        pg.display.set_icon(img)

    # config
    @property
    def title(self) -> str:
        return pg.display.get_caption()[0]

    @title.setter
    def title(self, value: str) -> None:
        pg.display.set_caption(value)

    @property
    def theme(self) -> ThemeManager:
        return self._theme

    @property
    def mouse_pos(self) -> tuple[int, int]:
        return self._mouse_pos

    def get_focus(self) -> GeometryManager | None:
        """
        get the currently focused item
        """
        return self._focus_item

    def set_focus(self, widget: tp.Union["GeometryManager", None, tp.Any] = None):
        """
        set the focused item
        """
        self._focus_item.stop_focus()

        if widget is not None:
            widget.set_focus()
            self._focus_item = widget

    def notify_focus(self, widget: tp.Union["GeometryManager", None] = None):
        """
        notify the root that a widget has been set as focus
        """
        if self._focus_item != widget:
            self.set_focus(widget)

    # interfacing
    def notify(self, event: ThemeManager.NotifyEvent, _info=...) -> None:
        """
        gets called by another class
        """
        match event:
            case ThemeManager.NotifyEvent.theme_reload:
                # the theme has been reloaded
                if not self._bg_configured:
                    self._bg = self.theme.root.bg.rgba

    # pygame stuff
    def _event_handler(self) -> None:
        """
        handle the events raised by pygame
        """
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self._running = False

                # case pg.VIDEORESIZE:  # window size changed
                #     width, height = event.size
                #
                #     print("updating size: ", (width, height), "\t", self._min_size)
                #
                #     width = max([width, self._min_size[0]])
                #     height = max([height, self._min_size[1]])
                #
                #     # self.__background = pg.display.set_mode((width, height), flags=pg.RESIZABLE | pg.HWSURFACE | pg.DOUBLEBUF)

        self._mouse_pos = pg.mouse.get_pos()

        self._notify_child_active_hover(self.mouse_pos)

    def update_screen(self) -> None:
        """
        update the screen
        """
        self.__background.fill(self._bg)

        self.calculate_geometry()
        for child, params in self._child_params:
            child.draw(self.__background)

        pg.display.flip()

    def update(self) -> None:
        """
        update events
        """
        self._event_handler()

    def mainloop(self):
        """
        run the windows main loop
        """
        while self._running:
            self.update()
            self.update_screen()

            self._clk.tick(self._max_framerate)

    def calculate_geometry(self):
        """
        calculate how each individual child should be placed
        """
        match self._layout:
            case Layout.Absolute:  # Absolute
                # since the positioning is absolute, the children should not influence the parents size
                for child, params in self._child_params:
                    child.set_position(params.x, params.y)

                return

            case Layout.Pack:
                directional_dict: dict[str, int | list] = {"total_x": 0, "total_y": 0, "children": [], "sizes": []}
                top = deepcopy(directional_dict)
                bottom = deepcopy(directional_dict)
                left = deepcopy(directional_dict)
                right = deepcopy(directional_dict)

                # get all sizes and group by anchor
                for child, param in self._child_params:
                    child_size = child.calculate_size()

                    if param.anchor == TOP:
                        top["children"].append(child)
                        top["sizes"].append(child_size)
                        top["total_x"] += child_size[0]
                        top["total_y"] += child_size[1]

                    elif param.anchor == BOTTOM:
                        bottom["children"].append(child)
                        bottom["sizes"].append(child_size)
                        bottom["total_x"] += child_size[0]
                        bottom["total_y"] += child_size[1]

                    elif param.anchor == LEFT:
                        left["children"].append(child)
                        left["sizes"].append(child_size)
                        left["total_x"] += child_size[0]
                        left["total_y"] += child_size[1]

                    elif param.anchor == RIGHT:
                        right["children"].append(child)
                        right["sizes"].append(child_size)
                        right["total_x"] += child_size[0]
                        right["total_y"] += child_size[1]

                top["total_y"] += self._layout_params.padding * len(top["children"]) - 1
                bottom["total_y"] += self._layout_params.padding * len(bottom["children"]) - 1

                left["total_x"] += self._layout_params.padding * len(left["children"]) - 1
                right["total_x"] += self._layout_params.padding * len(right["children"]) - 1

                min_x = max([top["total_x"], bottom["total_x"], left["total_x"] + right["total_x"]])
                min_y = max([left["total_y"], right["total_y"], top["total_y"] + bottom["total_y"]])

                # add margin
                min_x += self.layout_params.margin * 2
                min_y += self.layout_params.margin * 2

                self._min_size = min_x, min_y

                total_x, total_y = self.calculate_size()

                # tell the children where they should be
                y_cen = total_y / 2
                x_cen = total_x / 2

                # left
                x_now = self._layout_params.margin
                for child, size in zip(left["children"], left["sizes"]):
                    child.set_position(x_now, y_cen - size[1] / 2)
                    x_now += size[0] + self._layout_params.padding

                    # right
                x_now = total_x - self._layout_params.margin
                for child, size in zip(right["children"], right["sizes"]):
                    child.set_position(x_now - size[0], y_cen - size[1] / 2)
                    x_now -= size[0] + self._layout_params.padding

                    # top
                y_now = self._layout_params.margin
                for child, size in zip(top["children"], top["sizes"]):
                    child.set_position(x_cen - size[0] / 2, y_now)
                    y_now += size[1] + self._layout_params.padding

                    # bottom
                y_now = total_y - self._layout_params.margin
                for child, size in zip(bottom["children"], bottom["sizes"]):
                    child.set_position(x_cen - size[0] / 2, y_now - size[1])
                    y_now -= size[1] + self._layout_params.padding

            case Layout.Grid:
                rows: list[dict[str, tp.Any | float]] = []
                columns: list[dict[str, tp.Any | float]] = []

                for child, params in self._child_params:
                    row, column = params["row"], params["column"]

                    # if row was not yet made, make all previous ones
                    if len(rows) <= row:
                        for n_row in range(len(rows), row + 1):
                            out = {
                                "weight": 0,
                                "children": []
                            }

                            if n_row in self._grid_params.rows:
                                config = self._grid_params.rows[n_row]

                                if "weight" in config:
                                    out["weight"] = config["weight"]

                            rows.append(out)

                    if len(columns) <= column:
                        for n_col in range(len(columns), column + 1):
                            out = {
                                "weight": 0,
                                "children": []
                            }

                            if n_col in self._grid_params.columns:
                                config = self._grid_params.columns[n_col]

                                if "weight" in config:
                                    out["weight"] = config["weight"]

                            columns.append(out)

                    rows[row]["children"].append((child, params))
                    columns[column]["children"].append((child, params))

                matrix: list[list] = []

                for r in range(len(rows)):
                    matrix.append([])

                    for c in range(len(columns)):
                        # child = set(rows[r]["children"]) & set(columns[c]["children"])
                        child = [chi for chi in rows[r]["children"] if chi in columns[c]["children"]]
                        child = list(child)

                        if len(child) > 1:
                            raise ValueError(f"{len(child)} children assigned to row {r} column {c}!")

                        if child:
                            matrix[r].append(child[0])

                        else:
                            matrix[r].append(...)

                # calculate the minimal size for each row
                for r, row in enumerate(rows):
                    rows[r]["max_size"] = 0

                    for child, params in row["children"]:
                        _, y = child.calculate_size()

                        y += 2 * params.margin

                        if y > rows[r]["max_size"]:
                            rows[r]["max_size"] = y

                # calculate the minimal size for each column
                for c, column in enumerate(columns):
                    columns[c]["max_size"] = 0

                    for child, params in column["children"]:
                        x, _ = child.calculate_size()

                        x += 2 * params.margin

                        if x > columns[c]["max_size"]:
                            columns[c]["max_size"] = x

                    # calculate the container size
                width, height = self.calculate_size()

                # only subtract rows that don't have a weight
                min_width = sum([c["max_size"] for c in columns])
                min_height = sum([r["max_size"] for r in rows])

                # set the windows minimal size
                self._min_size = min_width, min_height

                # assign extra space
                extra_width = width - sum([c["max_size"] for c in columns if c["weight"] == 0])
                extra_height = height - sum([r["max_size"] for r in rows if r["weight"] == 0])

                total_row_weight = sum([row["weight"] for row in rows])
                total_column_weight = sum([column["weight"] for column in columns])

                # print(f"\n\nwindow_size=[{width}, {height}]\tmin_size={[min_width, min_height]}")
                # print(f"{total_row_weight=}")
                # print(f"{total_column_weight=}")
                # print(f"{extra_height=}")
                # print(f"{extra_width=}")

                # assign each row and column a specific size
                for r in range(len(rows)):
                    if total_row_weight == 0:
                        rows[r]["height"] = 0
                    else:
                        # assign either the minimum size or the calculated dynamic one
                        w_size = ((rows[r]["weight"] / total_row_weight) * extra_height).__floor__()
                        rows[r]["height"] = max([w_size, rows[r]["max_size"]])
                        # print(f"{w_size=}\t{rows[r]['max_size']=}")

                    # rows[r]["height"] += rows[r]["max_size"]
                    rows[r]["y_start"] = sum([prev_row["height"] for prev_row in rows[:r]])

                    for c in range(len(columns)):
                        if total_column_weight == 0:
                            columns[c]["width"] = 0
                        else:
                            # assign either the minimum size or the calculated dynamic one
                            w_size = ((columns[c]["weight"] / total_column_weight) * extra_width).__floor__()
                            columns[c]["width"] = max([w_size, columns[c]["max_size"]])
                            # print(f"{w_size=}\t{columns[c]['max_size']=}")

                        # columns[c]["width"] += columns[c]["max_size"]
                        columns[c]["x_start"] = sum([prev_col["width"] for prev_col in columns[:c]])

                        # pg.draw.rect(
                        #     self.__background,
                        #     (255, 0, 0, 255),
                        #     pg.Rect(columns[c]["x_start"], rows[r]["y_start"], columns[c]["width"], rows[r]["height"]),
                        #     width=1
                        # )

                # place children
                for child, params in self._child_params:
                    # place the child proportional to the table and stickiness
                    # size = list(child.calculate_size())
                    size = [child._width, child._height]

                    row, column = params["row"], params["column"]
                    sticky = params["sticky"]

                    width = columns[column]["width"]
                    height = rows[row]["height"]

                    x = columns[column]["x_start"]
                    y = rows[row]["y_start"]

                    x_cen = x + width / 2
                    y_cen = y + height / 2

                    x_diff = width - size[0]
                    y_diff = height - size[1]

                    # print(f"calc: {x_diff}, {y_diff}\t{size}\t{width},{height}")
                    # print(f"{sticky=}")

                    box_x = x_cen - size[0] / 2
                    box_y = y_cen - size[1] / 2

                    # assign stickiness
                    if not child._width_configured:
                        if "w" in sticky:
                            size[0] += (x_diff / 2) - params.margin
                            box_x = x + params.margin

                        if "e" in sticky:
                            size[0] += (x_diff / 2) - params.margin

                        child.assigned_width = size[0]

                    if not child._height_configured:
                        if "n" in sticky:
                            size[1] += (y_diff / 2) - params.margin
                            box_y = y + params.margin
                            # print("north: ", size, box_x, box_y, "\t\t", width, height)

                        if "s" in sticky:
                            size[1] += (y_diff / 2) - params.margin
                            # print("south: ", size, box_x, box_y, "\t\t", width, height)

                        child.assigned_height = size[1]

                    child.set_position(box_x, box_y)

            case _:
                raise ValueError(f"Invalid geometry type: {self._layout.__class__.__name__}")

    def calculate_size(self) -> tuple[int, int]:
        """
        calculate how big the container should be
        """
        # make sure the geometry is up-to-date
        return pg.display.get_window_size()
