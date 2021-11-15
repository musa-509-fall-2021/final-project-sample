import geopandas as gpd
import pandas as pd
from jinja2 import Environment, PackageLoader

def main(**kwargs):
    corridors_df = pd.read_gbq('SELECT * FROM final.corridors')
    corridors_df.geog = gpd.GeoSeries.from_wkt(corridors_df.geog)
    corridors_gdf = gpd.GeoDataFrame(corridors_df, geometry='geog')

    overview_df = pd.read_gbq('SELECT * from final.corridors_overview')

    env = Environment(loader=PackageLoader('generate_report'))
    template = env.get_template('index.html')
    print(template.render(
        corridors=corridors_gdf.to_dict('records')
    ))

if __name__ == '__main__':
    main()
