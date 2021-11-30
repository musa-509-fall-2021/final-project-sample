import geopandas as gpd
import pandas as pd
from pathlib import Path
from tempfile import NamedTemporaryFile
from jinja2 import Environment, PackageLoader
from pipeline_tools import local_file_to_gcs

def main(ds):
    # Get the data necessary for the report.
    corridors_df = pd.read_gbq('SELECT * FROM final.corridors')
    corridors_df.geog = gpd.GeoSeries.from_wkt(corridors_df.geog)
    corridors_gdf = gpd.GeoDataFrame(corridors_df, geometry='geog')

    # Load the templates.
    template_env = Environment(loader=PackageLoader('generate_report'))
    overview_template = template_env.get_template('index.html')
    corridor_template = template_env.get_template('corridor.html')

    # Determine the folder to save the rendered report pages into; create it if
    # it doesn't already exist. E.g.: report_generator/_reports/2021-11-22/
    output_folder = Path(__file__).parent / '_reports' / ds.isoformat()
    output_folder.mkdir(parents=True, exist_ok=True)

    # Write the overview.
    write_overview(corridors_gdf, overview_template, ds, output_folder)

    # Write each of the corridor-specific pages.
    corridors_gdf.apply(write_corridor, axis=1, args=[corridor_template, ds, output_folder])


def write_overview(corridors_gdf, template, ds, output_folder):
    overview_df = pd.read_gbq('SELECT * from final.corridors_overview')

    # Render the overview data into a template.
    output = template.render(
        corridors=corridors_gdf.to_dict('records'),
        overview=overview_df.to_dict('records')[0],
        overview_map_data=corridors_gdf.to_json(),
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


def write_corridor(corridor, template, ds, output_folder):
    # Render the corridor data into a tempate
    output = template.render(
        corridor=corridor.to_dict(),
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
    main(ds=dt.date.today())
