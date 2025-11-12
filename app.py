from __future__ import annotations

from dataclasses import dataclass
from typing import List

import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html


@dataclass(frozen=True)
class AutomatonParameters:
    s: float
    p_l_given_y: float
    p_y: float
    p_not_l_given_not_y: float

    @property
    def p_not_l_given_y(self) -> float:
        return 1.0 - self.p_l_given_y

    @property
    def p_not_y(self) -> float:
        return 1.0 - self.p_y

    @property
    def base_term(self) -> float:
        """Common bracket term appearing in the stationary distribution."""
        return (
            self.p_l_given_y * self.p_y
            + self.p_not_l_given_not_y * self.p_not_y
        )


def stationary_distribution(params: AutomatonParameters) -> List[float]:
    """
    Compute the stationary distribution for the eight-state literal automaton.

    The closed-form expressions are transcribed from the provided table where
    each πᵢ = α · P(Y)^{aᵢ} · P(¬L|Y)^{bᵢ} · P(L|Y)^{cᵢ} · s^{dᵢ} · B^{eᵢ}
    and B = P(L|Y)P(Y) + P(¬L|¬Y)P(¬Y). The normalising constant α ensures
    that the probabilities sum to one.
    """
    s = params.s
    py = params.p_y
    ply = params.p_l_given_y
    pnotly = params.p_not_l_given_y
    base = params.base_term

    terms = [
        py**4 * pnotly**7,
        py**3 * pnotly**6 * s * base,
        py**2 * pnotly**5 * s**2 * base**2,
        py * pnotly**4 * s**3 * base**3,
        pnotly**3 * s**4 * base**4,
        ply * pnotly**2 * s**5 * base**4,
        ply**2 * pnotly * s**6 * base**4,
        ply**3 * s**7 * base**4,
    ]

    total = sum(terms)
    if total == 0:
        # Avoid division by zero; fallback to uniform distribution.
        return [1.0 / len(terms)] * len(terms)

    alpha = 1.0 / total
    return [alpha * term for term in terms]


def create_figure(distribution: List[float]) -> go.Figure:
    states = [f"π{i}" for i in range(1, 9)]
    figure = go.Figure(
        data=[
            go.Bar(
                x=states,
                y=distribution,
                marker=dict(color="#1f77b4"),
                hovertemplate="%{x}: %{y:.4f}<extra></extra>",
            )
        ]
    )
    figure.update_layout(
        title="Literal Automaton Stationary Distribution",
        xaxis_title="State",
        yaxis_title="Probability",
        yaxis=dict(range=[0, max(distribution) * 1.1 if distribution else 1]),
        margin=dict(l=40, r=30, t=60, b=40),
        template="plotly_white",
    )
    return figure


def create_distribution_list(distribution: List[float]) -> html.Ul:
    return html.Ul(
        [
            html.Li(f"π{i + 1} = {value:.6f}")
            for i, value in enumerate(distribution)
        ],
        style={"columns": 2, "listStyleType": "none", "paddingLeft": 0},
    )


app = Dash(__name__)
app.title = "Literal Automaton Stationary Distribution"

app.layout = html.Div(
    [
        html.H1("Literal Automaton Stationary Distribution"),
        html.P(
            "Adjust the sliders to explore how the stationary distribution "
            "changes with the automaton parameters."
        ),
        html.Div(
            [
                html.Label("s"),
                dcc.Slider(
                    id="slider-s",
                    min=1.0,
                    max=25.0,
                    step=0.1,
                    value=10.0,
                    marks={1.0: "1", 10.0: "10", 25.0: "25"},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
                html.Label("P(L | Y)"),
                dcc.Slider(
                    id="slider-ply",
                    min=0.0,
                    max=1.0,
                    step=0.01,
                    value=0.5,
                    marks={0.0: "0.0", 0.5: "0.5", 1.0: "1.0"},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
                html.Label("P(Y)"),
                dcc.Slider(
                    id="slider-py",
                    min=0.0,
                    max=1.0,
                    step=0.01,
                    value=0.5,
                    marks={0.0: "0.0", 0.5: "0.5", 1.0: "1.0"},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
                html.Label("P(¬L | ¬Y)"),
                dcc.Slider(
                    id="slider-pnotl-noty",
                    min=0.0,
                    max=1.0,
                    step=0.01,
                    value=0.5,
                    marks={0.0: "0.0", 0.5: "0.5", 1.0: "1.0"},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ],
            style={"maxWidth": "600px"},
        ),
        html.Div(
            [
                dcc.Graph(id="stationary-bar"),
                html.Div(id="distribution-values"),
                html.Div(
                    id="derived-params",
                    style={"marginTop": "1rem", "fontFamily": "monospace"},
                ),
            ]
        ),
    ],
    style={"padding": "2rem", "fontFamily": "Arial, sans-serif"},
)


@app.callback(
    Output("stationary-bar", "figure"),
    Output("distribution-values", "children"),
    Output("derived-params", "children"),
    Input("slider-s", "value"),
    Input("slider-ply", "value"),
    Input("slider-py", "value"),
    Input("slider-pnotl-noty", "value"),
)
def update_visualisation(
    s: float,
    p_l_given_y: float,
    p_y: float,
    p_not_l_given_not_y: float,
):
    params = AutomatonParameters(
        s=s,
        p_l_given_y=p_l_given_y,
        p_y=p_y,
        p_not_l_given_not_y=p_not_l_given_not_y,
    )
    distribution = stationary_distribution(params)
    figure = create_figure(distribution)
    distribution_list = create_distribution_list(distribution)
    derived = html.Div(
        [
            html.Div(
                f"P(¬L | Y) = {params.p_not_l_given_y:.4f}, "
                f"P(¬Y) = {params.p_not_y:.4f}, "
                f"B = {params.base_term:.4f}"
            ),
        ]
    )
    return figure, distribution_list, derived


if __name__ == "__main__":
    app.run(debug=False)
