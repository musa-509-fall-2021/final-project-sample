import geopandas as gpd
import pandas as pd
from pathlib import Path
from tempfile import NamedTemporaryFile
from jinja2 import Environment, FileSystemLoader
from pipeline_tools import local_file_to_gcs

def main(ds):
    # Get the data necessary for the report.
    corridors_df = pd.read_gbq('SELECT * FROM final.corridor_details')
    corridors_df.geog = gpd.GeoSeries.from_wkt(corridors_df.geog)
    corridors_gdf = gpd.GeoDataFrame(corridors_df, geometry='geog')

    sqft_built_per_decade_df = pd.read_gbq('SELECT * from final.sqft_built_per_decade')
    sqft_updated_per_year_df = pd.read_gbq('SELECT * from final.sqft_updated_per_year')

    buildings_updated_df = pd.read_gbq('SELECT * FROM final.buildings_updated')
    buildings_updated_df.geog = gpd.GeoSeries.from_wkt(buildings_updated_df.geog)
    buildings_updated_gdf = gpd.GeoDataFrame(buildings_updated_df, geometry='geog')

    visits_per_day_df = pd.read_gbq('SELECT * from final.visits_per_day')

    # Load the templates.
    templates_folder = Path(__file__).parent / 'templates'
    template_env = Environment(loader=FileSystemLoader(templates_folder))
    overview_template = template_env.get_template('index.html')
    corridor_template = template_env.get_template('corridor.html')

    # Determine the folder to save the rendered report pages into; create it if
    # it doesn't already exist. E.g.: report_generator/_reports/2021-11-22/
    output_folder = Path(__file__).parent / '_reports' / ds
    output_folder.mkdir(parents=True, exist_ok=True)

    # Write the overview.
    write_overview(corridors_gdf, overview_template, ds, output_folder)

    # Write each of the corridor-specific pages.
    corridors_gdf.apply(write_corridor, axis=1, args=[
        corridor_template, ds, output_folder,
        corridors_gdf,
        sqft_built_per_decade_df,
        sqft_updated_per_year_df,
        buildings_updated_gdf,
        visits_per_day_df
    ])


def write_overview(corridors_gdf, template, ds, output_folder):
    overview_df = pd.read_gbq('SELECT * from final.corridors_overview')

    # Render the overview data into a template.
    output = template.render(
        corridors=corridors_gdf.to_dict('records'),
        most_healthy_corridors=corridors_gdf.nlargest(5, 'health').to_dict('records'),
        least_healthy_corridors=corridors_gdf.nsmallest(5, 'health').to_dict('records'),
        most_recently_built_corridors=corridors_gdf.nlargest(5, 'p50_year_built').to_dict('records'),
        least_recently_built_corridors=corridors_gdf.nsmallest(5, 'p50_year_built').to_dict('records'),
        most_recently_updated_corridors=corridors_gdf.nlargest(5, 'p50_last_permit_date').to_dict('records'),
        least_recently_updated_corridors=corridors_gdf.nsmallest(5, 'p50_last_permit_date').to_dict('records'),
        overview=overview_df.to_dict('records')[0],
        overview_map_data=corridors_gdf[['name', 'planning_district_name', 'filename', 'health_bin', 'geog']].to_json(),
    )

    # Write the report to the local folder, and upload to GCS.
    with open(output_folder / 'index.html', 'w') as local_file:
        local_file.write(output)
        local_file_to_gcs(
            local_file_name=local_file.name,
            gcs_bucket_name='mjumbewu_musa509_2021_corridors',
            gcs_blob_name=f'{ds}/index.html',
            content_type='text/html',
        )


def write_corridor(corridor, template, ds, output_folder,
                   corridors_gdf,
                   sqft_built_per_decade_df,
                   sqft_updated_per_year_df,
                   buildings_updated_gdf,
                   visits_per_day_df):
    import json
    import shapely.geometry

    # Filter data passed in from the main function to only what's relevent for
    # the current corridor.
    df = sqft_built_per_decade_df
    sqft_built_per_decade_df = df[df.corridorkey == corridor.corridorkey]

    df = sqft_updated_per_year_df
    sqft_updated_per_year_df = df[df.corridorkey == corridor.corridorkey]

    df = buildings_updated_gdf
    buildings_updated_gdf = df[df.corridorkey == corridor.corridorkey]

    df = visits_per_day_df
    visits_per_day_df = df[df.corridorkey == corridor.corridorkey]

    # Render the corridor data into a tempate
    output = template.render(
        corridor=corridor.to_dict(),
        corridors=corridors_gdf.to_dict('records'),
        corridor_map_center=corridor.geog.centroid,
        corridor_map_data=json.dumps(shapely.geometry.mapping(corridor.geog)),
        sqft_built_chart_data=sqft_built_per_decade_df.to_dict('list'),
        sqft_updated_chart_data=sqft_updated_per_year_df.to_dict('list'),
        buildings_updated_map_data=buildings_updated_gdf.to_json(),
        visits_chart_data=visits_per_day_df.to_dict('list'),
    )

    with open(output_folder / f'{corridor.filename}.html', 'w') as local_file:
        local_file.write(output)
        local_file_to_gcs(
            local_file_name=local_file.name,
            gcs_bucket_name='mjumbewu_musa509_2021_corridors',
            gcs_blob_name=f'{ds}/{corridor.filename}.html',
            content_type='text/html',
        )

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today().isoformat())
