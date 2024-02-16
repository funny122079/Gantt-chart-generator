[![Test](https://github.com/stefanSchinkel/gantt/actions/workflows/basic_test.yml/badge.svg)](https://github.com/stefanSchinkel/gantt/actions/workflows/basic_test.yml)

### README

Gantt is a python class to produce, well, Gantt charts. The charts are kept (very) simple, using a discreet time scale, unicolor bars and optional milesstones.

### Background

Gantt charts are commonly used in project management. I wanted to  make one myself and LibreProject was way too involved for the project in question. Hence I used OpenOffice Calc and made a plain horizontal bar chart. That took little time but was ok. Then I needed to add milestones (basically just a marker) to the chart. I completely failed doing this in OpenOffice (and still don't know how to do that ...).

Long story short: I don't know how to [excel](https://xkcd.com/559/).

### Basic usage

```python
from gantt import Gantt
g = Gantt('./sample.json')
g.render()
g.show()                # or save w/ g.save('foo.png')

```

Or simply call `runner.py`

### Data structure

All data is provided as a JSON structure that **has to contain**:

 - a key **packages** containing an array of package definitions with **label**, **end** and **start**. Start and end values are discreet.
 - a **title** string (may contain TeX, escaped)

```json
{
    "shifts": [
        {
            "name": "Jaspreet Singh",
            "scheduled_start": "05:00",
            "scheduled_end": "14:00",
            "start": "05:00",
            "end": "16:00",
            "break": 30
        },
        {
            "name": "Muskan Mahejan",
            "scheduled_start": "08:30",
            "scheduled_end": "14:00",
            "start": "08:30",
            "end": "14:00"
        },
        {
            "name": "Gagandeep Kaur",
            "scheduled_start": "09:30",
            "scheduled_end": "15:10",
            "start": "09:30",
            "end": "15:30"
        },
        {
            "name": "Anshika Anshika",
            "start": "15:30",
            "end": "22:00"
        },
        {
            "name": "Devarsh Agrawal",
            "scheduled_start": "15:00",
            "scheduled_end": "22:00",
            "start": "16:00",
            "end": "22:00",
            "break": 30
        },
        {
            "name": "Dhwani Soni",
            "start": "22:00",
            "end": "04:30",
            "break": 30
        },
        {
            "name": "Kenal Patel",
            "scheduled_start": "22:15",
            "scheduled_end": "06:30",
            "start": "22:00",
            "end": "06:30"
        }
    ]
}
```

The milestones, colors and legend entry are optional as are the label for the x-axis and the definition of the tickmarks.
The title may contain TeX, but make sure your system supports it. For

See [sample.json](./sample.json) for the data used to produce the image below.

### Installation

The requirements are rather limited and can installed from the requirements file. I recommend using a virtual environment for that:

```sh
# virtualenv setup, recommended
python3 -m venv .venv
source .venv/bin/activate
# actual install for requirements
pip install -r requirements.txt
# to install dev dependencies too run
# pip install -r requirements-dev.txt
```

### ToDo

 - nicer data structure (JSON) :white_check_mark:
 - dedicated class for packages :white_check_mark:
 - dynamic TeX support :white_check_mark:
 - add parameter object/dict for more control over colors etc :construction:

### Screenshot

![Sample Gantt with milestone](img/GANTT.png)

See [sample.json](./sample.json) for definition.

### Supported Versions

Support is a bit much to say. The initial version was developed on 3.6 and worked just fine. With github-actions I can only test 3.7+ and this works fine (up to 3.12 currently). But basically, if you get numpy/matplotlib to run, all should be fine.
