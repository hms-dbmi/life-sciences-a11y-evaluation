"""
Helpers to apply high-level themes to altair charts.
"""
def apply_theme(
    base,
    title_dy=-10,
    title_anchor="middle",
    title_font_size=20,
    subtitle_font_size=16,
    axis_title_font_size=16,
    axis_y_title_font_size=16,
    axis_label_font_size=16,
    axis_title_padding=10,
    axis_tick_color='white',
    axis_domain_width=1,
    label_angle=0,
    legend_orient="right",
    legend_title_orient="top",
    legend_stroke_color="transparent",
    legend_padding=0,
    legend_symbol_type="circle",
    legend_title_font_size=16,
    label_font_size=16,
    header_label_font_size=18,
    header_label_orient='top',
    point_size=70,
    gradient_length=50,
    x_label_angle=0,
    view_stroke_width=1
):
    return base.configure(
        font='Arial',
    ).configure_header(
        titleFontSize=20,
        titleFontWeight=500,
        labelOrient=header_label_orient,
        labelFontSize=header_label_font_size,
        labelFontWeight=500,
    ).configure_title(
        fontSize=title_font_size,
        subtitleFontSize=subtitle_font_size,
        subtitleColor='grey',
        fontWeight=500,
        anchor=title_anchor,
        align="left",
        dy=title_dy,
        subtitlePadding=10
    ).configure_axis(
        # domainWidth=2,
        labelFontSize=axis_label_font_size,
        labelFontWeight=400,
        titleFontSize=axis_title_font_size,
        titleFontWeight=500,
        labelLimit=1000,
        labelPadding=10,
        titlePadding=axis_title_padding,
        tickColor=axis_tick_color,
        domainWidth=axis_domain_width,
        domainColor='black',
        ticks=False
        # labelAngle=label_angle
    ).configure_scale(
        # bandPaddingOuter=0.5
    ).configure_axisX(
        labelAngle=x_label_angle
    ).configure_axisY(
        titleFontSize=axis_y_title_font_size,
        domain=False
    ).configure_legend(
        titleFontSize=legend_title_font_size,
        titleFontWeight=500,
        labelFontSize=label_font_size,
        labelFontWeight=400,
        padding=legend_padding,
        cornerRadius=0,
        orient=legend_orient,
        fillColor="white",
        symbolStrokeWidth=2,
        strokeColor=legend_stroke_color,
        # temporally commented out
        # symbolType=legend_symbol_type,
        titleOrient=legend_title_orient,
        # direction='horizontal',
        gradientLength=gradient_length
    ).configure_concat(
        spacing=0
    ).configure_view(
        fill='#F5F5F5',  #'transparent', # ', # '#F6F6F6', # '#F5F5F5', '#FBFBFB'
        strokeWidth=view_stroke_width,
        stroke='white'
        # strokeWidth=2
    ).configure_point(
        size=point_size
    )