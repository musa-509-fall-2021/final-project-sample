0.  [x] Brainstorm for aspects of your proposal
1.  [ ] Develop metrics that will help inform the domain decisions
1.  [x] Get familiar with the content of potential datasets; understand what might inform your metrics, and what holes there still are
    - [x] Corridor health
    - Buildings
      - [x] Median age of buildings in each corridor
      - [ ] Distribution of building age (grouped by 5-year increments)
      - [ ] Distribution of building update age (grouped by 5-year increments)
      - [ ] Corridor need of renovation: median building/update age -- low (under 5 years), medium (5-15 years), high (over 15 years)
    - Businesses
      - [ ] Number of businesses (by category)
      - [ ] Age of businesses
      - [ ] Share of owners that live within 2 miles (requires a geocoder 🙁)
      - [ ] Diversity of businesses: how many business categories have at least (2? 3?) businesses?
    - Engagement
      - [ ] Distance from home block group histogram (for visitors from Philadelphia)
1.  [x] Consider best way to communicate metrics; for example:
    - Should you use time-series graphs? Density/heat-maps? You're certainly not limited in the number of visualizations you can include.
    - Should your report only be at one level of detail, or should you include a break-down by sub-geography (neighborhood, district, etc)?
1.  [x] Write proposal and develop wireframes
    * Include boxes for metrics and sample prose on wireframes
1.  [x] Develop scripts to extract data from sources and load into PostgreSQL and/or BigQuery
1.  [x] Create the structure for your Airflow pipeline and add your extract/load scripts to it
1.  [ ] Deploy your pipeline to a cloud server (and document your deployment steps for _when_ -- not _if_ -- you forget them)
1.  [x] Dive deeper into data
    * Experiment and develop queries for metrics, using tools such as PGAdmin, BigQuery, or Jupyter Notebooks
    * Note useful data transformations and queries
1.  [ ] Convert explorations into SQL and Python scripts to transform ingested data
1.  [ ] Experiment with visualizations of metrics
1.  [ ] Create "live mockup(s)" in HTML of dashboard page(s)
1.  [x] Configure a GCS
1.  [ ] Convert mockup(s) to template(s)
1.  [ ] Create scripts to render template(s) for dashboard page(s)
