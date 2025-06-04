::: {#0 .cell .markdown editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
<div class="demo-info">

# Agile Metabolic Health Blood Pressure Dashboard Demo

Note: this cell has custom styling that makes it **not** show up in the Voilà Dashboard. 
You can hide any other markdown in this notebook by surrounding it with the same "demo-info"
class ID as this one.

This dashboard fetches and displays blood pressure data for a patient.

(DEMO) To edit the dashboard:

1. <a href="#" id="demo-edit-link" target="demo-edit">click here</a> to open the notebook
1. edit the notebook
1. save changes
1. reload this page

To add goals to the demo, add `include_goal=True` to the last cell in this notebook to select a patient, edit the cell below that sets `patient_id` , `study_id`. You can see values in the [JupyterHealth Exchange Portal](https://http://berkeley-jhe-staging.jupyterhealth.org/portal/studies).

</div>
<script type="text/javascript">
var link = document.getElementById("demo-edit-link");
link.href = document.location.href.replace("/voila/render/", "/lab/tree/")
</script>
<style type="text/css">
.demo-info {
    font-style: italic;
    /* hide all the demo info */
    display: none;
}

.added-widget {
    /* add some highlighting for widgets added in the demo */
    font-weight: bold;
    background-color: rgb(220, 255, 220) !important;
}

</style>
:::

::: {#1 .cell .code editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
``` python
import os

import ipywidgets as W
from IPython.display import HTML, Image, Markdown, display


# Convenience function to display markdown
def md(s):
    display(Markdown(s))


# Use "if not VOILA:" blocks to print debug/private output
# Otherwise all output is by default shown by VOILA
VOILA = os.environ.get("VOILA_REQUEST_URL")
```
:::

::: {#2 .cell .code editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
``` python
from jupyterhealth_client import Code, JupyterHealthClient

client = JupyterHealthClient()
BLOOD_PRESSURE = Code.BLOOD_PRESSURE.value
user_info = client.get_user()
```
:::

::: {#3 .cell .code editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
``` python
from functools import lru_cache

from requests import HTTPError

_width = "500px"


@lru_cache
def _cache_fetch_data(study_id, patient_id):
    """Cache fetching the same data"""
    return client.list_observations_df(
        patient_id=patient_id, study_id=study_id, code=Code.BLOOD_PRESSURE
    )


study_widget = W.Dropdown(
    options=[],
    layout=W.Layout(width=_width),
    description="Study",
)


def _update_study_list(change=None):
    value = study_widget.value
    options = {}
    for study in client.list_studies():
        label = f"[{study['id']}] {study['name']}"
        options[label] = study["id"]
    if not options:
        options["<no available studies>"] = None
    study_widget.options = options
    if value not in options.values():
        study_widget.value = next(iter(options.values()))


_update_study_list()

patient_widget = W.Dropdown(
    options=[],
    description="Patient",
    layout=W.Layout(width=_width),
)


def _update_patient_list(change=None):
    value = patient_widget.value
    options = {}
    for patient in client.list_patients():
        label = f"{patient['nameFamily']}, {patient['nameGiven']}: {patient['telecomEmail']}"
        options[label] = patient["id"]
    if not options:
        options["<no available patients>"] = None
    patient_widget.options = options
    if value not in options.values():
        patient_widget.value = next(iter(options.values()))


_update_patient_list()

# uncomment to add 'demo-info' class, which hides these from the rendered dashboard
# study_widget.add_class("demo-info")
# patient_widget.add_class("demo-info")

patient_df = None


def _load_data(change=None):
    global patient_df
    if not study_widget.value or not patient_widget.value:
        patient_df = None
        return
    try:
        patient_df = _cache_fetch_data(study_widget.value, patient_widget.value)
    except (ValueError, HTTPError):
        patient_df = None
    if patient_df is not None and len(patient_df) == 0:
        patient_df = None


patient_widget.observe(_load_data, names="value")
_load_data()

try:
    study_widget.value = 30013  # Jupyter Study
    patient_widget.value = 40039  # test user
except Exception:
    print(
        "Failed to set default study/patient. May not have access. Are you a member of the BIDS organization?"
    )

refresh_button = W.Button(
    description="Refresh patients and studies", layout=W.Layout(width=_width)
)


def _reload(btn=None):
    _update_study_list()
    _update_patient_list()


refresh_button.on_click(_reload)

display(study_widget)
display(patient_widget)
display(refresh_button)
```
:::

::: {#4 .cell .code editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
``` python
if not VOILA:
    if patient_df is None or not len(patient_df):
        raise ValueError("Found no observations!")
    display(patient_df.head())
```
:::

::: {#5 .cell .code editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
``` python
# now start the plotting

from datetime import timedelta
from enum import Enum
from functools import partial
from itertools import chain

import altair as alt
import pandas as pd

pd.options.mode.chained_assignment = None


class Goal(Enum):
    """Enum for met/unmet

    These strings will be used for the legend.
    """

    met = "under"
    unmet = "over"


class Category(Enum):
    normal = "normal"
    elevated = "elevated"
    hypertension = "hypertension"


def classify_bp(row):
    """Classify blood pressure"""
    # https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings
    # note from : We can decide to have just normal, elevated and hypertension to begin with
    if (
        row.diastolic_blood_pressure_value < 80
        and row.systolic_blood_pressure_value < 120
    ):
        return Category.normal.value
    elif (
        row.diastolic_blood_pressure_value < 80
        and 120 <= row.systolic_blood_pressure_value < 130
    ):
        return Category.elevated.value
    else:
        return Category.hypertension.value


def bp_goal(patient_df, goal="140/90"):
    """True/False for blood pressure met goal"""
    sys_goal, dia_goal = (int(s) for s in goal.split("/"))
    if (patient_df.systolic_blood_pressure_value <= sys_goal) & (
        patient_df.diastolic_blood_pressure_value <= dia_goal
    ):
        return Goal.met.value
    else:
        return Goal.unmet.value


red_yellow_blue = [
    "#4a74b4",
    "#faf8c1",
    "#d4322c",
]
red_blue = [red_yellow_blue[0], red_yellow_blue[-1]]


def bp_over_time(bp, color_scale="category"):
    """Plot blood pressure over time"""
    # https://vega.github.io/vega/docs/schemes/#redyellowblue
    if color_scale == "category":
        domain = [
            Category.normal.value,
            Category.elevated.value,
            Category.hypertension.value,
        ]
        color = alt.Color(
            "category:O",
            scale=alt.Scale(
                domain=domain,
                range=red_yellow_blue,
            ),
        )
        shape = alt.Shape(
            "category:O",
            scale=alt.Scale(
                domain=domain,
            ),
        )
    elif color_scale == "goal":
        domain = [Goal.met.value, Goal.unmet.value]
        color = alt.Color(
            "goal:O",
            scale=alt.Scale(domain=domain, range=red_blue),
        )
        shape = alt.Shape(
            "goal:O",
            scale=alt.Scale(domain=domain),
        )

    # heuristic for x-ticks
    end_time = bp.effective_time_frame_date_time.max()
    end_date = end_time.date()
    start_date = bp.effective_time_frame_date_time.min().date()
    time_frame_days = (end_date - start_date).total_seconds() / (3600 * 24)
    axis_args = {"format": "%Y-%m-%d"}
    if time_frame_days < 7:
        # minimum of one week
        start_date = end_date - timedelta(days=7)
    if time_frame_days < 14:
        # at least a week
        axis_args["tickCount"] = dict(interval="day", step=1)
    if 14 <= time_frame_days < 30:
        # expand less than a month to 1 month
        start_date = end_date - timedelta(days=30)
    if time_frame_days > 90:
        # at least a few months, label with year-month
        axis_args["format"] = "%Y-%m"

    x = alt.X(
        "effective_time_frame_date_time_local",
        title="date",
        axis=alt.Axis(
            labelAngle=30,
            **axis_args,
        ),
        scale=alt.Scale(
            domain=[
                pd.to_datetime(start_date),
                pd.to_datetime(end_date + timedelta(days=1)),
            ]
        ),
    )

    charts = [
        [
            alt.Chart(bp, title="blood pressure")
            .mark_line(color="#333")
            .encode(
                x=x,
                y=alt.Y(f"{which}_blood_pressure_value", title="mmHg"),
            ),
            alt.Chart(bp, title="blood pressure")
            .mark_point(filled=True)
            .encode(
                x=x,
                y=alt.Y(f"{which}_blood_pressure_value", title="mmHg"),
                color=color,
                shape=shape,
                tooltip=[
                    alt.Tooltip("effective_time_frame_date_time_local", title="date"),
                    alt.Tooltip("systolic_blood_pressure_value", title="Systolic"),
                    alt.Tooltip("diastolic_blood_pressure_value", title="Diastolic"),
                    alt.Tooltip("category"),
                ],
            ),
        ]
        for which in ("systolic", "diastolic")
    ]
    return alt.layer(*chain(*charts))


def bp_by_tod(bp):
    """Plot blood pressure by time of day"""
    tod_tooltip = [
        alt.Tooltip(
            "mean(diastolic_blood_pressure_value):Q",
            title="avg diastolic",
            format=".0f",
        ),
        alt.Tooltip(
            "mean(systolic_blood_pressure_value):Q", title="avg systolic", format=".0f"
        ),
        alt.Tooltip("count(diastolic_blood_pressure_value)", title="measurements"),
        alt.Tooltip("hours(effective_time_frame_date_time_local)", title="hour"),
    ]
    charts = [
        alt.Chart(bp, title="by time of day")
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "hours(effective_time_frame_date_time_local)",
                title="time of day",
                scale=alt.Scale(domain=[0, 24]),
            ),
            y=alt.Y(
                f"mean({which}_blood_pressure_value):Q",
                title=which,
                axis=alt.Axis(title=""),
            ),
            tooltip=tod_tooltip,
        )
        for which in ("systolic", "diastolic")
    ]
    return alt.layer(*charts)


def plot_patient_blood_pressure(patient_df, goal="140/90", color_scale="category"):
    """plot blood pressure, given a patient data frame, as returned by get_patient_data"""
    bp = patient_df.loc[patient_df.resource_type == BLOOD_PRESSURE]
    bp["category"] = bp.apply(classify_bp, axis=1)
    bp["goal"] = bp.apply(partial(bp_goal, goal=goal), axis=1)
    return (
        (bp_over_time(bp, color_scale=color_scale) | bp_by_tod(bp))
        .resolve_scale(y="shared", color="independent", shape="independent")
        .configure_point(size=100)
        .interactive()
    )


if not VOILA:
    # show last 30 days of data
    end_date = patient_df.effective_time_frame_date_time.max()
    display(
        plot_patient_blood_pressure(
            patient_df[patient_df.effective_time_frame_date_time >= (end_date - timedelta(days=30))],
            color_scale="goal",
        )
    )
```
:::

::: {#6 .cell .code editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
``` python
import ipywidgets as W


def bp_category_style(row):
    """highlight rows by bp category"""
    category = Category(row.category)
    if category == Category.hypertension:
        color = "#fdd"
    elif category == Category.elevated:
        color = "#ffc"
    else:
        color = None

    return [f"background-color:{color}" if color else None] * len(row)


def bp_goal_style(row):
    """highlight rows by bp category"""
    goal = Goal(row.goal)
    if goal == Goal.unmet:
        color = "#fdd"
    else:
        color = None

    return [f"background-color:{color}" if color else None] * len(row)


def bp_goal_fraction(patient_df, goal="140/90"):
    bp = patient_df.loc[patient_df.resource_type == BLOOD_PRESSURE]
    sys_goal, dia_goal = (int(s) for s in goal.split("/"))
    met_goal = (bp.systolic_blood_pressure_value <= sys_goal) & (
        bp.diastolic_blood_pressure_value <= dia_goal
    )
    return met_goal.sum() / len(bp)


def bp_table_info(patient_df, goal="140/90", color_scale="category"):
    """Display tabular info"""
    bp = patient_df.loc[
        patient_df.resource_type == BLOOD_PRESSURE,
        [
            "effective_time_frame_date_time_local",
            "systolic_blood_pressure_value",
            "diastolic_blood_pressure_value",
        ],
    ]
    bp["category"] = bp.apply(classify_bp, axis=1)
    bp["goal"] = bp["goal"] = bp.apply(partial(bp_goal, goal=goal), axis=1)
    # relabel columns
    bp.columns = ["date", "systolic", "diastolic", "category", "goal"]
    bp["time"] = bp.date.dt.time
    bp["date"] = bp.date.dt.date
    bp = bp.astype({"systolic": int, "diastolic": int})

    label_style = {"font_weight": "bold", "font_size": "150%"}

    table = W.Output()
    with table:
        styled = (
            bp.style.hide()
            .hide(["category", "goal"], axis="columns")
            .format({"time": "{:%H:%M}"})
        )
        if color_scale == "goal":
            styled = styled.apply(bp_goal_style, axis=1)
        else:
            styled = styled.apply(bp_category_style, axis=1)
        display(HTML(styled.to_html(index=False)))

    summary = W.Output()
    min_idx = bp.systolic.idxmin()
    max_idx = bp.systolic.idxmax()
    summary_table = pd.DataFrame(
        {
            "systolic": [
                bp.systolic.min(),
                bp.systolic.max(),
                bp.systolic.mean(),
            ],
            "diastolic": [
                bp.diastolic.min(),
                bp.diastolic.max(),
                bp.diastolic.mean(),
            ],
            "date": [
                bp.loc[min_idx].date,
                bp.loc[max_idx].date,
                "-",
            ],
        }
    )
    summary_table = summary_table.astype({"systolic": int, "diastolic": int})
    summary_table.index = pd.Index(["min", "max", "avg"])
    with summary:
        display(HTML(summary_table.to_html()))

    # calculate goal fraction
    at_goal_fraction = bp_goal_fraction(patient_df, goal)
    overview = W.Output()
    with overview:
        display(
            HTML(f"<div style='font-size: 250%'>at goal: {at_goal_fraction:.0%}</div>")
        )

    box_layout = {
        "border_left": "1px solid #aaa",
        "padding": "8px",
        "margin": "8px",
    }
    right_box = [
        W.Label(value="summary", style=label_style),
        summary,
    ]
    if color_scale == "goal":
        right_box.extend(
            [
                W.Label(value="overview", style=label_style),
                overview,
            ]
        )
    layout = W.HBox(
        [
            W.VBox(
                [W.Label(value="Measurements", style=label_style), table],
                layout=box_layout,
            ),
            W.VBox(
                right_box,
                layout=box_layout,
            ),
        ]
    )
    layout.layout.justify_content = "flex-start"
    return layout


if not VOILA:
    # preview while run interactively (not voila)
    display(bp_table_info(patient_df[-100:], color_scale="goal"))
```
:::

::: {#7 .cell .code editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
``` python
import time


def plot_patient(
    view=30,
    comorbidity=False,
    color="goal",
):
    if comorbidity:
        goal = "130/80"
    else:
        goal = "140/90"
    df = patient_df
    if df is None:
        patient_id = patient_widget.value
        study_id = study_widget.value

        if not patient_id:
            md("## No patient selected!")
            return

        if not study_id:
            md("## No study selected!")
            return

        consents = client.get_patient_consents(patient_id)
        md_lines = [f"## No data for patient {patient_id} in study {study_id}!", ""]

        md_lines.append("Study consents:")
        for study in consents["studies"]:
            md_lines.append(f"  - [{study['id']}] {study['name']}")
        if not consents["studies"]:
            md_lines.append("- (none)")
        md_lines.append("")

        md_lines.append("Studies pending consent:")
        md_lines.append("")
        for study in consents["studiesPendingConsent"]:
            md_lines.append(f"  - [{study['id']}] {study['name']}")
        if not consents["studiesPendingConsent"]:
            md_lines.append("- (none)")
        md_lines.append("")
        md("\n".join(md_lines))
        return

    last_day = df.effective_time_frame_date_time.dt.date.max()
    start_date = last_day - timedelta(days=view)
    df = df[df.effective_time_frame_date_time.dt.date >= start_date]
    # for demo: scale if current user is too healthy
    df = df.copy()
    df["systolic_blood_pressure_value"] = (df["systolic_blood_pressure_value"]).astype(
        int
    )
    df["diastolic_blood_pressure_value"] = (
        df["diastolic_blood_pressure_value"]
    ).astype(int)
    display(plot_patient_blood_pressure(df, goal=goal, color_scale=color))
    display(bp_table_info(df, goal=goal, color_scale=color))
    # utterly bizarre: voilá hangs if this returns too quickly
    time.sleep(0.5)


if not VOILA:
    plot_patient()
```
:::

::: {#8 .cell .markdown editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
<div class="demo-info">

---
    
Everything above here is setup of the demo itself, not part of the demo; this would all be hidden and managed by EHR inputs.

Below here is the actual demo that is meant to show up as a dashboard and meant for display.
</div>
:::

::: {#9 .cell .code editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
``` python
# create the interactive chart


def create_dashboard(include_goal=False):
    """
    Create the dashboard

    only one input: include_goal
    if True, include UCSF goal inputs ('after' view)
    if False, only include American Heart Association category view
    """

    interact_args = {}
    if include_goal:
        comorbidity_widget = W.Checkbox(
            description="Any comorbidities: ASCVD > 10%, Diabetes Mellitus, CKD (EGFR 20-59), Heart Failure"
        )
        comorbidity_widget.layout.width = "100%"
        comorbidity_widget.add_class("added-widget")
        color_widget = W.Dropdown(
            value="goal", options={"UCSF Goal": "goal", "AHA Category": "category"}
        )
        color_widget.add_class("added-widget")
        interact_args["comorbidity"] = comorbidity_widget
        interact_args["color"] = color_widget
    else:
        interact_args["comorbidity"] = W.fixed(False)
        interact_args["color"] = W.fixed("category")

    dashboard = W.interactive(
        plot_patient,
        view={
            "Week": 7,
            "Month": 30,
            "Year": 365,
        },
        **interact_args,
    )
    # give it some border to set it off from the demo setup
    dashboard.layout.border = "4px solid #cff"
    dashboard.layout.padding = "16px 30px"

    # rerender on change of widgets outside the interact
    patient_widget.observe(lambda change: dashboard.update(), names="value")
    study_widget.observe(lambda change: dashboard.update(), names="value")
    return dashboard
```
:::

::: {#10 .cell .markdown editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
## Agile Metabolic JupyterHealth Dashboard
:::

::: {#11 .cell .code}
``` python
md("#### Logged in as practitioner:")
md(f"{user_info['firstName']} {user_info['lastName']} ({user_info['email']})")
md("---")
```
:::

::: {#12 .cell .code editable="true" slideshow="{\"slide_type\":\"\"}" tags="[]"}
``` python
# DEMO: uncomment include_goal=True to add UCSF goals to visualization,
create_dashboard(
    include_goal=True,
)
```
:::

::: {#13 .cell .code}
``` python
# weird: displaying this in a Markdown cell
# causes voila to hang (?!)
display(Image(url="https://jupyterhealth.org/images/PoweredByJupyter.png"))
```
:::
