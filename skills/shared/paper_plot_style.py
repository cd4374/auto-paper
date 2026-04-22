"""
Publication-quality plotting style for auto-paper.

Usage:
    from shared.paper_plot_style import *

Constants:
    STYLE: 'publication' (default), 'poster', 'slide'
    DPI: 300
    FORMAT: 'pdf' (vector), 'png' (raster fallback)
    COLOR_PALETTE: 'tab10', 'Set2', 'colorblind' (deuteranopia-safe)
    FONT_SIZE: 10 (base font size, matches typical conference body text)
    FIG_DIR: 'figures/' (output directory)
"""

import os
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm

# ============================================================================
# Constants
# ============================================================================

STYLE = 'publication'  # Options: publication, poster, slide
DPI = 300
FORMAT = 'pdf'  # Options: pdf (vector), png (raster)
COLOR_PALETTE = 'tab10'  # Options: tab10, Set2, colorblind
FONT_SIZE = 10
FIG_DIR = 'figures/'
FONT_FAMILY = 'serif'

# Poster style: larger fonts
POSTER_FONT_SIZE = 14
# Slide style: even larger, bolder colors
SLIDE_FONT_SIZE = 16

# ============================================================================
# Color Palettes
# ============================================================================

COLOR_PALETTES = {
    'tab10': plt.cm.tab10.colors,
    'Set2': plt.cm.Set2.colors,
    'colorblind': ['#0173b2', '#de8f05', '#029e73', '#cc78bc', '#ca9161',
                   '#949494', '#ece133', '#56b4e9', '#d55e00', '#0173b2'],
}


def _get_font_size():
    """Get font size based on style."""
    if STYLE == 'poster':
        return POSTER_FONT_SIZE
    elif STYLE == 'slide':
        return SLIDE_FONT_SIZE
    return FONT_SIZE


def _get_axes_params():
    """Get axes parameters based on style."""
    fs = _get_font_size()
    return {
        'font.size': fs,
        'font.family': FONT_FAMILY,
        'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
        'axes.labelsize': fs,
        'axes.titlesize': fs + 1,
        'xtick.labelsize': fs - 1,
        'ytick.labelsize': fs - 1,
        'legend.fontsize': fs - 1,
        'figure.dpi': DPI,
        'savefig.dpi': DPI,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,
        'axes.grid': False,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'text.usetex': False,
        'mathtext.fontset': 'stix',
    }


# Apply default style
matplotlib.rcParams.update(_get_axes_params())

# Color palette
COLORS = COLOR_PALETTES.get(COLOR_PALETTE, plt.cm.tab10.colors)


# ============================================================================
# Utility Functions
# ============================================================================

def setup_style(style='publication'):
    """
    Setup matplotlib style for publication/poster/slide.

    Args:
        style: 'publication', 'poster', or 'slide'
    """
    global STYLE
    STYLE = style
    matplotlib.rcParams.update(_get_axes_params())


def save_fig(fig, name, fmt=FORMAT, fig_dir=FIG_DIR):
    """
    Save figure to FIG_DIR with consistent naming.

    Args:
        fig: matplotlib figure object
        name: output filename (without extension)
        fmt: 'pdf' or 'png'
        fig_dir: output directory

    Example:
        >>> fig, ax = plt.subplots()
        >>> ax.plot([1, 2, 3], [1, 4, 9])
        >>> save_fig(fig, 'fig2_training_curves')
    """
    os.makedirs(fig_dir, exist_ok=True)
    path = os.path.join(fig_dir, f'{name}.{fmt}')
    fig.savefig(path)
    print(f'Saved: {path}')


def add_subfigure_label(ax, label, pos='top_left'):
    """
    Add (a), (b), (c)... label to subplot.

    Args:
        ax: matplotlib axes object
        label: 'a', 'b', 'c', ... or number 1, 2, 3, ...
        pos: 'top_left' or 'top_right'

    Example:
        >>> fig, (ax1, ax2) = plt.subplots(1, 2)
        >>> add_subfigure_label(ax1, 'a')
        >>> add_subfigure_label(ax2, 'b')
    """
    label_str = chr(ord('a') + int(label) - 1) if isinstance(label, int) else label
    positions = {
        'top_left': (-0.1, 1.05),
        'top_right': (1.02, 1.05),
    }
    x, y = positions.get(pos, (-0.1, 1.05))
    ax.text(x, y, f'({label_str})', transform=ax.transAxes,
            fontsize=FONT_SIZE + 2, fontweight='bold',
            va='top', ha='left')


def create_figure(width='single', height_ratio=0.7, nrows=1, ncols=1):
    """
    Create a figure with standard publication sizes.

    Args:
        width: 'single' (0.48\\textwidth) or 'double' (0.95\\textwidth)
        height_ratio: height / width ratio
        nrows: number of rows
        ncols: number of columns

    Returns:
        fig, axes tuple

    Example:
        >>> fig, ax = create_figure('single')
        >>> fig, axes = create_figure('double', nrows=2, ncols=2)
    """
    # Approximate text width for single column (3.5-6 inches)
    widths = {
        'single': 5,
        'double': 10,
    }
    w = widths.get(width, 5)
    h = w * height_ratio
    fig, axes = plt.subplots(nrows, ncols, figsize=(w, h))
    if nrows == 1 and ncols == 1:
        axes = [axes]
    return fig, axes


def finalize_figure(fig, tight=True):
    """
    Finalize figure with tight layout.

    Args:
        fig: matplotlib figure object
        tight: whether to apply tight_layout
    """
    if tight:
        fig.tight_layout()


# ============================================================================
# Figure Type Reference
# ============================================================================

"""
| Type          | When to Use                    | Typical Size     |
|---------------|--------------------------------|------------------|
| Line plot     | Training curves, scaling       | 0.48\\textwidth  |
| Bar chart     | Method comparison, ablation    | 0.48\\textwidth  |
| Grouped bar   | Multi-metric comparison        | 0.95\\textwidth  |
| Scatter plot  | Correlation analysis           | 0.48\\textwidth  |
| Heatmap       | Attention, confusion matrix    | 0.48\\textwidth  |
| Box/violin    | Distribution comparison        | 0.48\\textwidth  |
| Multi-panel   | Combined results (subfigures)  | 0.95\\textwidth  |
| Comparison    | Prior bounds vs. ours (theory) | full width       |

Chart type decision tree:
1. X = time/steps, Y = metric → Line plot
2. X = category, Y = value → Bar chart
3. X = continuous, Y = continuous → Scatter plot
4. Matrix/grid values → Heatmap
5. Distribution → Box/violin plot
6. Multi-dataset/multi-method → Multi-panel (subfigure)
"""
