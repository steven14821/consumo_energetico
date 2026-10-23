import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ── Página ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Optimización del consumo energético · Centro de datos",
    page_icon=":zap:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colores (tema neutro, estilo Apple) ─────────────────────────────────────
BG_SURFACE   = "#FFFFFF"
BG_SIDEBAR   = "#F7F8FA"
BG_PLOT      = "#F4F5F6"
TEXT_PRIMARY = "#111111"
TEXT_SECONDARY = "#333333"
TEXT_MUTED   = "#555555"
BORDER       = "#DDDDDD"
ACCENT       = "#1A5F8A"
GREEN        = "#1B8A5A"
RED          = "#C23B2E"
BLUE         = "#1B6BFF"

# ── CSS (Tailwind + Apple-style custom layer) ──────────────────────────────────────────────
# Framework: Tailwind CSS (CDN). No local install required.
# Apple-style custom layer: fix pixel-perfect details Tailwind doesn't cover.
st.markdown(
    """
    <style>
    /* ───────────────────────────────────────────────────────────────────────── */
    /* 1. FRAMEWORK: Tailwind CSS  (CDN, zero install)                          */
    /* ───────────────────────────────────────────────────────────────────────── */
    @import url('https://cdn.tailwindcss.com');

    /* ───────────────────────────────────────────────────────────────────────── */
    /* 2. APPLE-STYLE COLOR THEME (neutral, clean, data-focused)                */
    /* ───────────────────────────────────────────────────────────────────────── */
    :root {
        --bg-surface:  #FFFFFF;
        --bg-sidebar:  #F7F8FA;
        --bg-plot:     #F4F5F6;
        --text-primary:#111111;
        --text-secondary:#333333;
        --text-muted:  #555555;
        --border:      #DDDDDD;
        --accent:      #1A5F8A;
        --accent-soft: #E6F0F4;
        --glass-bg:    rgba(255,255,255,0.72);
        --glass-border: rgba(0,0,0,0.08);
    }

    /* ───────────────────────────────────────────────────────────────────────── */
    /* 3. BASE LAYOUT (font stack, page chrome, print)                          */
    /* ───────────────────────────────────────────────────────────────────────── */
    html, body {
        margin: 0;
        padding: 0;
        background: var(--bg-surface);
        color: var(--text-primary);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    body {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        line-height: 1.4;
    }

    /* ───────────────────────────────────────────────────────────────────────── */
    /* 4. NAVIGATION CHROME (override Streamlit defaults)                       */
    /* ───────────────────────────────────────────────────────────────────────── */
    .stApp-header { background: rgba(255,255,255,0.85) !important; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid var(--glass-border) !important; }
    .stApp-viewer { background: var(--bg-surface) !important; }
    .stSidebar { background: var(--glass-bg) !important; backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid var(--glass-border) !important; border-radius: 24px; }
    .stSidebar .section { background: rgba(255,255,255,0.4) !important; border-radius: 16px; padding: 0.75rem 1rem; }
    .stAppHeaderButton { color: var(--text-primary) !important; }
    .stAppHeaderButton:hover { background: var(--glass-border) !important; }
    .stApp-header .stAppHeaderButton svg { fill: var(--text-primary) !important; }
    .stApp-header { border-bottom: 1px solid var(--border); }

    /* ───────────────────────────────────────────────────────────────────────── */
    /* 5. SIDEBAR STRUCTURE                                                     */
    /* ───────────────────────────────────────────────────────────────────────── */
    .stSidebar .section { margin-top: 0.5rem !important; }
    .stSidebar .stSelectbox, .stSidebar .stNumberInput, .stSidebar .stCheckbox, .stSidebar .stRadio { margin-bottom: 0.75rem !important; }

    /* ── Subheader labels (uppercase, letter-spaced) ──────────────────────── */
    .sidebar-title {
        color: var(--text-primary);
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.25rem;
    }
    .sidebar-subheader {
        color: var(--text-primary);
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.6px;
        margin-top: 0.9rem;
        margin-bottom: 0.45rem;
    }

    /* ── Separator line ───────────────────────────────────────────────────── */
    .sep {
        height: 1px;
        background: var(--border);
        border: none;
        margin: 1.2rem 0;
    }

    /* ───────────────────────────────────────────────────────────────────────── */
    /* 6. METRIC CARDS (rounded, soft shadow, hover lift)                       */
    /* ───────────────────────────────────────────────────────────────────────── */
    .metric-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.6);
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover { border-color: var(--accent); box-shadow: 0 12px 48px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.6); }
    .metric-card + .metric-card { margin-top: 0.9rem; }

    .metric-label {
        color: var(--text-primary);
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }

    .metric-unit {
        font-size: 0.85rem;
        color: var(--text-secondary);
        font-weight: 600;
        margin-left: 4px;
    }

    /* ── Semantic badges (pill shaped, uppercase) ─────────────────────────── */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.85rem;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
        background: var(--glass-bg);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid var(--glass-border);
    }
    .badge-green { background: #E6F4EA; color: #0F6B2E; }
    .badge-amber { background: #FEF3E2; color: #8A5200; }
    .badge-red   { background: #FCEAEB; color: #B02A1E; }

    /* ───────────────────────────────────────────────────────────────────────── */
    /* 7. CONTROLS (slider accent, knob, labels)                               */
    /* ───────────────────────────────────────────────────────────────────────── */
    .stSlider label { font-size: 1rem; font-weight: 600; color: var(--text-primary); }
    .stSlider .slider-container { background: rgba(0,0,0,0.06); border-radius: 999px; padding: 0.3rem; }
    .stSlider .slider-track-fill { accent-color: var(--accent); border-radius: 999px; }
    .stSlider .slider-thumb { accent-color: var(--accent); transform: scale(1.2); border-radius: 999px; }
    .stSlider .slider-track-fill { accent-color: var(--accent); border-radius: 4px; }
    .stSlider .slider-thumb { accent-color: var(--accent); transform: scale(1.15); }
    .stSlider .slider-track { border-radius: 4px; }
    .stSlider input[type=range] { vertical-align: middle; }

    /* ───────────────────────────────────────────────────────────────────────── */
    /* 8. CHART CONTAINER (white rounded card)                                 */
    /* ───────────────────────────────────────────────────────────────────────── */
    .chart-container {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 1.2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.6);
    }
    .chart-container + .chart-container { margin-top: 0.8rem; }

    /* Plotly specific refinements */
    .plotly .plotly-graph-div { background: var(--bg-surface); }
    .plotly .modebar { background: rgba(255,255,255,0.9) !important; }

    /* ───────────────────────────────────────────────────────────────────────── */
    /* 9. FOOTER                                                              */
    /* ───────────────────────────────────────────────────────────────────────── */
    .footer {
        margin-top: 1.5rem;
        font-size: 0.82rem;
        color: var(--text-secondary);
        line-height: 1.6;
        background: var(--glass-bg);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
    }

    /* ───────────────────────────────────────────────────────────────────────── */
    /* 10. SCROLLBAR (thin, neutral)                                           */
    /* ───────────────────────────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-plot); border-radius: 4px; }
    ::-webkit-scrollbar-thumb { background: #C9D1D7; border-radius: 4px; border: 1px solid var(--border); }
    ::-webkit-scrollbar-thumb:hover { background: #A8B2BA; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Título ───────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 class='text-3xl font-bold text-[#1D1D1F] tracking-tight'>Optimización del consumo energético</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='text-base text-[#57606A] mt-1 leading-relaxed'>"
    "Ajusta el punto de operación con los controles y compara el consumo real "
    "contra el óptimo teórico. La línea punteada define la capacidad térmica del rack.</p>",
    unsafe_allow_html=True,
)

# ── Panel lateral ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div class='text-xs font-bold uppercase tracking-widest text-[#8A9098] mb-3'>"
        "Punto de operación (x, y)</div>",
        unsafe_allow_html=True,
    )
    x = st.slider("Temperatura de consigna", 0.0, 8.0, 3.0, 0.1, key="x")
    y = st.slider("Velocidad de ventiladores", 0.0, 14.0, 5.0, 0.1, key="y")

    st.markdown(
        "<div class='text-xs font-bold uppercase tracking-widest text-[#8A9098] mb-3 mt-4'>"
        "Comparación</div>",
        unsafe_allow_html=True,
    )

    E_current = 300 + 2*x**2 - x*y + y**2 - 15*x - 12*y

    p_current  = (3, 5)
    p_opt_livre = (6, 9)
    p_opt_rest  = (4, 7)
    E_p_current  = 300 + 2*p_current[0]**2 - p_current[0]*p_current[1] + p_current[1]**2 - 15*p_current[0] - 12*p_current[1]
    E_p_opt_livre = 300 + 2*p_opt_livre[0]**2 - p_opt_livre[0]*p_opt_livre[1] + p_opt_livre[1]**2 - 15*p_opt_livre[0] - 12*p_opt_livre[1]
    E_p_opt_rest  = 300 + 2*p_opt_rest[0]**2 - p_opt_rest[0]*p_opt_rest[1] + p_opt_rest[1]**2 - 15*p_opt_rest[0] - 12*p_opt_rest[1]

    delta_pct = (E_current - E_p_opt_livre) / E_p_opt_livre * 100

    st.metric("E(x, y) actual", f"{E_current:.1f}", "kW")
    st.metric("E(3,5) base", f"{E_p_current:.1f}", "kW")
    st.metric("E(6,9) óptimo libre", f"{E_p_opt_livre:.1f}", "kW")
    st.metric("E(4,7) óptimo restringido", f"{E_p_opt_rest:.1f}", "kW")

    if delta_pct < 0:
        badge = "<span class='badge badge-green'>Mejor que el óptimo libre</span>"
    elif delta_pct < 5:
        badge = "<span class='badge badge-amber'>Cerca del óptimo libre</span>"
    else:
        badge = "<span class='badge badge-red'>Lejos del óptimo</span>"
    st.metric("Diferencia vs óptimo libre", f"{delta_pct:.1f}%", badge)

    st.markdown(
        "<div class='text-xs font-bold uppercase tracking-widest text-[#8A9098] mb-3 mt-4'>"
        "Comprobación</div>",
        unsafe_allow_html=True,
    )
    st.caption("3x + y = " + str(round(3*x + y, 1)) + "   |   límite térmico = 19")

# ── Cálculo de la función ───────────────────────────────────────────────────
x_grid = np.linspace(0, 8, 400)
y_grid = np.linspace(0, 14, 400)
X, Y = np.meshgrid(x_grid, y_grid)
E_grid = 300 + 2*X**2 - X*Y + Y**2 - 15*X - 12*Y

# Línea de restricción térmica
x_rest = np.linspace(0, 8, 200)
y_rest = 19 - 3*x_rest

# ── Gráfico principal ───────────────────────────────────────────────────────
fig = go.Figure()

# Superficie de contornos
fig.add_trace(
    go.Contour(
        z=E_grid,
        x=x_grid,
        y=y_grid,
        colorscale=[
            [0.0,  "#D5F5E3"],
            [0.35, "#A5D6A7"],
            [0.6,  "#FFB300"],
            [0.85, "#FF8A65"],
            [1.0,  "#C62828"],
        ],
        showscale=False,
        contours=dict(
            start=400, end=1100, size=25,
            labelfont=dict(size=10, color="#546E7A"),
        ),
        hovertemplate="x=%{x:.2f} °C<br>y=%{y:.2f} ×100 rpm<br>E=%{z:.1f} kW<extra></extra>",
    )
)

# Línea de restricción térmica
fig.add_trace(
    go.Scatter(
        x=x_rest, y=y_rest,
        mode="lines",
        line=dict(color="#FEB72C", width=3, dash="dash"),
        name="Límite térmico 3x + y = 19",
        hovertemplate="Límite térmico<br>3x + y = 19<extra></extra>",
    )
)

# Punto actual (P₁ rojo)
fig.add_trace(
    go.Scatter(
        x=[p_current[0]], y=[p_current[1]],
        mode="markers+text",
        marker=dict(size=16, color=RED, line=dict(color="white", width=2)),
        text=["P₁"],
        textposition="top center",
        textfont=dict(size=14, color=RED, weight="bold"),
        hovertemplate="Punto actual<br>x = 3.0 °C<br>y = 5.0 ×100 rpm<br>E = 223.0 kW<extra></extra>",
    )
)

# Óptimo libre (P₂ verde)
fig.add_trace(
    go.Scatter(
        x=[p_opt_livre[0]], y=[p_opt_livre[1]],
        mode="markers+text",
        marker=dict(size=16, color=GREEN, line=dict(color="white", width=2)),
        text=["P₂"],
        textposition="bottom center",
        textfont=dict(size=14, color=GREEN, weight="bold"),
        hovertemplate="Óptimo libre<br>x = 6.0 °C<br>y = 9.0 ×100 rpm<br>E = 201.0 kW<extra></extra>",
    )
)

# Óptimo restringido (P₃ azul)
fig.add_trace(
    go.Scatter(
        x=[p_opt_rest[0]], y=[p_opt_rest[1]],
        mode="markers+text",
        marker=dict(size=16, color=BLUE, line=dict(color="white", width=2)),
        text=["P₃"],
        textposition="top center",
        textfont=dict(size=14, color=BLUE, weight="bold"),
        hovertemplate="Óptimo restringido<br>x = 4.0 °C<br>y = 7.0 ×100 rpm<br>E = 209.0 kW<extra></extra>",
    )
)

# Punto móvil (P negro)
fig.add_trace(
    go.Scatter(
        x=[x], y=[y],
        mode="markers+text",
        marker=dict(size=18, color=ACCENT, line=dict(color="white", width=2)),
        text=["P"],
        textposition="top center",
        textfont=dict(size=14, color=ACCENT, weight="bold"),
        hovertemplate="Punto seleccionado<br>x = %{x:.2f} °C<br>y = %{y:.2f} ×100 rpm<br>E = %{customdata[0]:.1f} kW<extra></extra>",
        customdata=np.array([[E_grid[np.argmin(np.abs(y_grid - y)), np.argmin(np.abs(x_grid - x))]]]),
    )
)

# Etiqueta del valor en el punto móvil
fig.add_trace(
    go.Scatter(
        x=[x], y=[y],
        mode="text",
        text=[f"E = {E_grid[np.argmin(np.abs(y_grid - y)), np.argmin(np.abs(x_grid - x))]:.1f} kW"],
        textposition="bottom center",
        textfont=dict(size=14, color=ACCENT, weight="bold"),
        showlegend=False,
    )
)

fig.update_layout(
    title="Curvas de nivel de E(x, y) · Optimización de consumo energético",
    xaxis_title="Temperatura de consigna ΔT (°C)",
    yaxis_title="Velocidad de ventiladores (cientos de rpm)",
    xaxis=dict(range=[0, 8], zeroline=False),
    yaxis=dict(range=[0, 14], zeroline=False),
    height=580,
    width=800,
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    hovermode="closest",
    legend=dict(
        yanchor="bottom", y=0.02, xanchor="right", x=0.98,
        bordercolor="#DADCE0", borderwidth=1, bgcolor="white",
    ),
)

st.plotly_chart(fig, use_container_width=True)

# ── Métricas laterales ─────────────────────────────────────────────────────
st.markdown(
    "<div class='text-xs font-bold uppercase tracking-widest text-[#8A9098] mb-4 mt-12'>"
    "Métricas en tiempo real</div>",
    unsafe_allow_html=True,
)

val_movil = E_grid[np.argmin(np.abs(y_grid - y)), np.argmin(np.abs(x_grid - x))]

# Punto actual
st.markdown(
    f"<div class='metric-card'>"
    f"<span class='metric-label'>Punto actual</span>"
    f"<span class='metric-value'>{val_movil:.1f}</span>"
    f"<span class='metric-unit'>kW</span></div>",
    unsafe_allow_html=True,
)

# Óptimo libre
st.markdown(
    f"<div class='metric-card'>"
    f"<span class='metric-label'>Óptimo libre (sin restricción)</span>"
    f"<span class='metric-value'>{E_p_opt_livre:.1f}</span>"
    f"<span class='metric-unit'>kW · verde</span></div>",
    unsafe_allow_html=True,
)

# Óptimo restringido
st.markdown(
    f"<div class='metric-card'>"
    f"<span class='metric-label'>Óptimo restringido (Lagrange)</span>"
    f"<span class='metric-value'>{E_p_opt_rest:.1f}</span>"
    f"<span class='metric-unit'>kW · azul</span></div>",
    unsafe_allow_html=True,
)

# Diferencia vs óptimo libre
diff = val_movil - E_p_opt_livre
if diff < 0:
    badge_class = "badge-green"
elif diff < 5:
    badge_class = "badge-amber"
else:
    badge_class = "badge-red"
st.markdown(
    f"<div class='metric-card'>"
    f"<span class='metric-label'>Diferencia vs óptimo libre</span>"
    f"<span class='metric-value' style='color:#0B7285'>{diff:.1f} kW</span>"
    f"<span class='metric-unit'>· <span class='badge {badge_class}'>{badge_class.replace('badge-', '').title()}</span></span>"
    f"</div>",
    unsafe_allow_html=True,
)

# Rango
st.markdown(
    f"<div class='metric-card'>"
    f"<span class='metric-label'>Rango de E(x,y)</span>"
    f"<span class='metric-value'>{E_grid.min():.0f}</span>"
    f"<span class='metric-unit'>–</span>"
    f"<span class='metric-value'>{E_grid.max():.0f}</span>"
    f"<span class='metric-unit'>kW</span></div>",
    unsafe_allow_html=True,
)

# Constante térmica
st.markdown(
    f"<div class='metric-card'>"
    f"<span class='metric-label'>Constante térmica actual (3x + y)</span>"
    f"<span class='metric-value'>{3*x + y:.1f}</span>"
    f"<span class='metric-unit'>/ 19</span></div>",
    unsafe_allow_html=True,
)

# ── Pie de página ──────────────────────────────────────────────────────────
st.markdown("<hr class='sep'>", unsafe_allow_html=True)
st.markdown(
    "<p class='footer'>"
    "<strong>E(x, y)</strong> = 300 + 2x² − xy + y² − 15x − 12y,  "
    "con 0 ≤ x ≤ 8 (°C) y 0 ≤ y ≤ 14 (cientos de rpm).  "
    "La línea punteada delimita la capacidad térmica máxima del rack."
    "</p>",
    unsafe_allow_html=True,
)
