# FlightAware KML Extract

Quick and dirty extraction script.

2024-12-03. Will break when FlightAware changes their output page
appreciably.

1. Go to a FlightAware page.

2. Click `View track log`.

3. Save HTML.

4. Run this script:

   ```
   ./flightaware_extract.py input.html > output.kml
   ```
