# The Illusion of the Average Neighborhood

This project is a static data-visualization webpage about crime patterns in San Francisco. It argues that neighborhood-level averages can hide the real structure of crime, which is often concentrated in a small number of places and shaped by policing patterns as much as by offense patterns.

The main page presents three connected visual stories:

1. Spatial concentration of theft in small geographic blocks.
2. Hourly and weekly rhythms in crime reporting and enforcement.
3. A heatmap that illustrates how enforcement-heavy data can create misleading feedback loops.

The project is built as a single HTML page with embedded CSS and JavaScript, plus a few generated visualization files and image assets.

## Project Structure

- `index.html` - Main narrative page.
- `images/` - Static images used in the article, such as plots and charts.
- `visualizations/` - Standalone interactive visualization pages embedded into the main page with `iframe`.
- `README.md` - Project documentation.

## How To Run

This is a static website, so there is no build step.

### Option 1: Open directly

Open `index.html` in a browser.

### Option 2: Run a local server

Using a local server is recommended, especially if the browser blocks some local file resources.

From the project folder:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

If you want to serve only this project folder, make sure your terminal is inside `marijn-118.github.io` before starting the server.

## Dependencies

There is no package manager setup and no install step. The page relies on:

- Browser support for standard HTML, CSS, JavaScript, and `iframe`.
- External CDN-hosted libraries used by the exported visualizations, such as Plotly and Leaflet.

Because of those CDN links, the visualizations work best when the machine has internet access.

## Data And Content Notes

- The content is based on San Francisco crime incident data from SF OpenData.
- The narrative references research on predictive policing, data bias, and narrative visualization.
- The page is written as a self-contained story, so the visual design and the explanatory text are part of the deliverable, not just supporting documentation.

## Deployment

This repository is suitable for GitHub Pages because it is a static site. If you publish it there, GitHub Pages should serve `index.html` as the homepage automatically.

## Editing

If you change the content or visuals:

- Keep image paths in `index.html` aligned with the files in `images/`.
- Keep the `iframe` paths aligned with files in `visualizations/`.
- If you regenerate the embedded charts, make sure the exported HTML files keep working as standalone pages.

## License

No license file is currently included. Add one if you want to define reuse terms explicitly.
