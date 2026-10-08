# care-calendar

Generates a yearly child custody calendar as a single HTML page.

For each day of the year, the calendar shows who has the children (`B` or `L`),
and the handovers (e.g. `B→L`). Guardians are computed from the custody rules of
the court order, which are hard-coded in `kaloot/custody.py` and described in
`comments.md`. Public holidays are computed automatically; school holidays and
custom arrangements come from a yearly configuration file.

The published calendars live in `docs/`, one folder per year.


## Requirements

- [uv](https://docs.astral.sh/uv/) (dependencies are installed automatically on first run)
- `make`


## Generating the calendar for a year

The example below uses 2029.

1. **Create the configuration file** at the root of the repository, starting from
   the previous year's:

   ```bash
   cp config-2028.yaml config-2029.yaml
   ```

2. **Edit `config-2029.yaml`**: set `year: 2029` and update the school holidays
   (see [Configuration](#configuration) below).

3. **Build it**:

   ```bash
   make 2029
   ```

   This writes `docs/2029/` with:
   - `calendar-2029.html`: the calendar,
   - `index.html`: a link to `calendar-2029.html`,
   - copies of `config-2029.yaml` and `comments.md`, to keep track of what the
     calendar was generated from.

   A `make <year>` target exists for every `config-<year>.yaml` at the root. Running
   it again simply regenerates the calendar.

4. **Check the result** by opening `docs/2029/calendar-2029.html` in a browser.

5. **Run the tests**:

   ```bash
   make test
   ```

When the dates of the remaining school holidays are announced later in the year,
update the configuration and run `make <year>` again.


## Publishing

`docs/` is the published website. `docs/index.html` (the home page) is a link to the
current year's calendar.

1. If the new year should become the home page, point `docs/index.html` to it:

   ```bash
   ln -sf 2029/index.html docs/index.html
   ```

2. Commit the configuration file and the generated folder, then push:

   ```bash
   git add config-2029.yaml docs/2029 docs/index.html
   git commit -m "2029"
   git push origin main
   ```

Only the configuration of the year in progress needs to stay at the root. To
regenerate an older year, copy its configuration back from `docs/<year>/` first.


## Configuration

```yaml
# Markdown text displayed below the calendar.
comments: comments.md

# Directory containing the HTML templates and CSS.
template_dir: templates

year: 2029

# Example dates: use the official ones.
Vacances scolaires:
  css_class: "vacancesscolaires"
  dates:
    - 22/12/2028 - 07/01/2029   # Christmas holidays, spanning two years
    - 10/02 - 25/02             # winter
    - 07/04 - 22/04             # spring
    - 07/07 - 31/08             # summer
    - 20/10 - 04/11             # autumn

# Optional: days on which the parents agreed on a different arrangement.
custom:
  css_class: "customcare"
  dates:
    - dates: 01/01 - 04/01
      care: B
    - dates: 14/03
      care: L
```

- **Dates** are written `dd/mm`, using the configuration's `year`, or `dd/mm/yyyy`
  (`dd/mm/yy` also works) when they belong to another year. A range is written
  `start - end`; both days are included.
- **`Vacances scolaires`** lists the school holidays of the children's academy,
  using the official dates. The holidays that span the new year are written with
  explicit years.
- **`custom`** (optional) overrides the computed guardian. Each entry has `dates`
  (a day or a range) and `care` (`B` or `L`). Handovers are added automatically
  at the boundaries of each custom period. Custom days are highlighted and listed
  in the legend.
- **Public holidays** (including Easter, Ascension and Pentecost) are computed
  automatically and need no configuration.

Colors are defined in `templates/calendar.css`, using the `css_class` names above.
