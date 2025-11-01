from enum import Enum


class warapiEndpoints(Enum):
    war_state = r"/worldconquest/war"
    # may be updated every 60 seconds
    map_list = r"/wolrdconquest/maps"
    # not all maps have available map data
    map_war_report = r"/worldconquest/warReport/{map_name}"
    # may be updated every 3 seconds
    static_map_data = r"/worldconquest/maps/{map_name}/static"
    # needs to be done once per war
    dynamic_map_data = r"/worldconquest/maps/{map_name}/dynamic/public"
    # may be updated every 3 seconds
    map_data_schema = r"/worldconquest/maps/{map_name}/static"
    # no info on update refresh time
