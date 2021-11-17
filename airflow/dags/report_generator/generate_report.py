import geopandas as gpd
import pandas as pd
from jinja2 import Environment, PackageLoader

def main():
    corridors_df = pd.read_gbq('SELECT * FROM final.corridors')
    corridors_df.geog = gpd.GeoSeries.from_wkt(corridors_df.geog)
    corridors_gdf = gpd.GeoDataFrame(corridors_df, geometry='geog')

    overview_df = pd.read_gbq('SELECT * from final.corridors_overview')

    env = Environment(loader=PackageLoader('generate_report'))
    template = env.get_template('index.html')
    output = template.render(
        corridors=corridors_gdf.to_dict('records'),
        overview=overview_df.to_dict('records')[0],
        overview_map_data=corridors_gdf.to_json(),
    )
    return output

if __name__ == '__main__':
    print(main())
