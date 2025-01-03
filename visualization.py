import plotly.graph_objects as go

def plot_payoff(S, K, option_type='call'):
    payoff = [max(0, s - K) if option_type == 'call' else max(0, K - s) for s in S]

    # Determine X-axis range dynamically based on strike price
    x_min = min(S[0], K)
    x_max = max(S[-1], K)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=payoff, mode='lines', name='Payoff'))
    fig.update_layout(
        title="",
        xaxis_title="Stock Price",
        yaxis_title="Payoff",
        template="plotly_white",
        margin=dict(l=0, r=0, t=30, b=30),
        yaxis=dict(range=[-50, 50]),
        xaxis=dict(range=[x_min, x_max]),
    )
    return fig
