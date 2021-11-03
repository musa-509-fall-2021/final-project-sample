## Abstract

**Who is it for:** Community groups to advocate for their main streets. City officials to identify places where additional resources might be helpful.

**How will they use it:** The commerce department needs to keep track of the health of business districts month after month. Each quarter, during their strategic planning, this dashboard will serve as a central artifact for discussing where funds may need to be focused, and for assessing the impact of previous interventions. Overall, the trends surfaced with this dashboard will allow Commerce to take a more iterative approach to community development, by having a more up-to-date view on the data.

Because the pace of change for a business district can be slow, and because patterns of change in public space are often seasonal, the dashboard will focus mainly on year-over-year change for a handful of metrics. In particular:
- foot traffic (when and how much)
- internal and facade renovations (how prevalent and how recent)
- diversity of businesses
- local ownership of businesses

These metrics will allow stakeholders to target different programs at each district. For example:
- low rates of local business ownership may prompt business education programs for community residents
- increasing average time since
- low foot traffic in the face of other positively trending metrics may prompt public space activation events

## Data sources

- **L&I business licenses** -- [OpenDataPhilly](https://opendataphilly.org/dataset/licenses-and-inspections-business-licenses), updated regularly
- **L&I building and zoning permits** -- [OpenDataPhilly](https://opendataphilly.org/dataset/licenses-and-inspections-building-permits), updated regularly
- **City commercial corridors** -- [OpenDataPhilly](https://opendataphilly.org/dataset/commercial-corridors/resource/b8cf80de-88af-4eb7-9392-95980fef319b)
- **SafeGraph foot traffic** -- Available in bulk downloads, but uncertain from the API. Ideally I would set up a [monthly delivery](https://docs.safegraph.com/docs/bulk-data-delivery) from SafeGraph, but it's uncertain if that's available on an academic account. May simulate that for now, by manually extracting latest extract to GCS each month.
- **US Census Block Group demographics** -- BigQuery public datasets
