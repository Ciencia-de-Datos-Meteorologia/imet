from print_names import print_names
from plot_points import plot_points
from extend_bounds import extend_bounds
from extend_palette import extend_palette
from plot_shapes import plot_shapes


import os
import shapefile
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import image, offsetbox
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import cartopy.feature as cfeature
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

from . import placesprint as pp




# map plotting function
def array_to_plot(mapdata, lat, lon, outpath, figname, settings, utilitiespath, show,
                    foottext:bool=True, logo:bool=True, logoinmap:bool=True,
                    clip_to_dep:bool=False):

    # default colors
    seablue = '#87CEFA'
    mapgray = '#cccccc'

    # settings unpacking
    pal = settings['pal']
    bound = settings['bounds']
    ticks = settings['ticks']
    ticklabels = settings['ticklabels']
    ticks_text = settings['ticks_text']
    colorspt = settings['colorspt']
    ext = settings['ext']
    loc = settings['locate']
    title = settings['title']
    infot = settings['info']
    datafromtxt = settings['datafrom']
    section = settings['section']
    infocolor = settings['info_color']

    # locate # extent of map
    if not loc:
        latmax = 18.1
        latmin = 13.6
        lonmax = -88.2
        lonmin = -92.3
    elif isinstance(loc, str):
        latmax, lonmin, latmin, lonmax, prep_max, depa, muni = pp.iregions[loc]
    elif isinstance(loc, list):
        lonmin = loc[0]
        lonmax = loc[1]
        latmin = loc[2]
        latmax = loc[3]
    else:
        raise ValueError('bad locate parameter, pass list of coordinates (lonmin, lonmax, latmin, latmax) or the name of a preset')

    # color map
    if isinstance(pal, str):
        cmap = mpl.cm.get_cmap(pal)
        # alternative
        # cmap = plt.cm.get_cmap(pal)
    elif isinstance(pal, list):
        cmap = mpl.colors.ListedColormap(extend_palette(pal, colorspt, ext))

    # color bar
    if colorspt is not None:
        norm = mpl.colors.BoundaryNorm(extend_bounds(bound, colorspt, ext, cmap.N), cmap.N)

    ###########################################################################
    # figure initialization
    plt.figure()

    # axes projection and extent
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([lonmin, lonmax, latmin, latmax])
    # margins around data
    ax.set_xmargin(0.00)
    ax.set_ymargin(0.00)

    # map color mesh (data)
    im = plt.pcolormesh(lon, lat, mapdata, cmap=cmap, transform=ccrs.PlateCarree(),
                        norm=norm, zorder=2)
    # color bar
    cb = plt.colorbar(im, ticks=bound, extend=ext)

    # color bar ticks
    if ticks is not None:
        cb.set_ticks(ticks)
    if ticklabels is not None:
        cb.set_ticklabels(ticklabels)

    # color bar tick labels
    cb.set_label(ticks_text, rotation=-90, fontsize=9, va='baseline', labelpad=14)

    # gridlines
    if not loc or loc=='CA':
        step = 1 if not loc else 3
        # gridline locators
        ylocator = np.arange(np.floor(latmin), np.ceil(latmax), step)
        xlocator = np.arange(np.floor(lonmin), np.ceil(lonmax), step)
    elif isinstance(loc, (str, list)):
        # gridline locators
        ylocator = np.around(np.linspace(np.floor(latmin), np.ceil(latmax), 6), decimals=2)
        xlocator = np.around(np.linspace(np.floor(lonmin), np.ceil(lonmax), 6), decimals=2)

    # draw gridlines
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.7,
                        color='gray', alpha=0.7, linestyle='--', zorder=4)
    gl.top_labels = False
    gl.right_labels = False
    gl.ylocator = mticker.FixedLocator(ylocator)
    gl.xlocator = mticker.FixedLocator(xlocator)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size':6, 'color':'black'}
    gl.ylabel_style = {'size':6, 'color':'black'}

    ###########################################################################
    # features

    # path to maps
    path_mapas = os.path.join(utilitiespath, 'maps/')

    # oceans
    oceans = cfeature.NaturalEarthFeature(category='physical', name='ocean', scale='10m',
                                            facecolor=seablue)
    ax.add_feature(oceans, zorder=3)

    # country masks
    earthsf = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_0_countries')
    earthreader = shpreader.Reader(earthsf)
    countries = earthreader.records()
    # masked countries are different for CA maps
    countries_masked = ['MEX', 'BLZ', 'SLV', 'HND' ] if loc!='CA' else ['MEX', 'COL', 'JAM', 'CYM']
    # get geometries of masked countries
    for country in countries:
        if country.attributes['ADM0_A3'] in countries_masked:
            # add_geometries requires an iterable
            # country geometry may be a MultiPolygon (iterable), a Polygon (non iterable), ...
            geometry = country.geometry
            try:
                iter(geometry)
            except TypeError:
                geometry = [geometry]
            # mask
            ax.add_geometries(geometry, ccrs.PlateCarree(), facecolor=mapgray, zorder=3)

    # draw shapes
    if loc=='CA':
        # country borders # all countries
        plot_shapes(os.path.join(path_mapas, "Americas/Americas.shp"), ax, color='black', lw=0.8)
    else:
        # country borders # except Guate
        plot_shapes(os.path.join(path_mapas, "america/America.shp"), ax, color='black', lw=0.8)

        # Guatemala shape # with departments
        plot_shapes(os.path.join(path_mapas, "GUATE_WGS84.shp"), ax, color='black', lw=1)

        # lakes
        plot_shapes(os.path.join(path_mapas, "lakes/Principales_lagos.shp"), ax, color='black', lw=0.8,
                    fill=True, fcolor=seablue)

    # Belice border
    plot_shapes(os.path.join(path_mapas, "Lim_Belice/Lim_Belice.shp"), ax, color=mapgray, lw=1, ls='dotted')

    # clip to depto
    if clip_to_dep and isinstance(loc, (str, int)) and loc!='CA':
        # show that we clippin'
        print('with clip loc')

        # convert number to department names
        locregions = {'centro':[1, 3, 4], 'surocc':[10, 11], 'CE':[1, 3, 4], 'CE2':[1, 4]}
        try:
            intdept = [int(loc)]
        except:
            intdept = locregions[loc]

        # this file is different to GUATE_WGS84
        # munisf = shapefile.Reader(os.path.join(path_mapas, 'muni/Municipios_340_dd.shp'))
        # depas = []
        # for shape in munisf.shapeRecords():
        #     if shape.record[3] in intdept:
        #         depas.append(plt.Polygon(shape.shape.points, color='w', ec='k'))

        # TEMPORARY FIX: country shape's deparments are different from muni shapes
        deptdict = {'Guatemala':1, 'El Progreso':2, 'Sacatepquez':3, 'Chimaltenango':4, 'Escuintla':5,
                    'Santa Rosa':6, 'Solol':7, 'Totonicapn':8, 'Quetzaltenango':9, 'Suchitepquez':10,
                    'Retalhuleu':11, 'San Marcos':12, 'Huehuetenango':13, 'Quich':14, 'Baja Verapaz':15,
                    'Alta Verapaz':16, 'Petn':17, 'Izabal':18, 'Zacapa':19, 'Chiquimula':20,
                    'Jalapa':21, 'Jutiapa':22}
        #
        munisf = shapefile.Reader(os.path.join(path_mapas, "GUATE_WGS84.shp"))
        depas = []
        for shape in munisf.shapeRecords():
            if shape.record[0] and deptdict[shape.record[0]] in intdept:
                depas.append(plt.Polygon(shape.shape.points, color='w', ec='k'))

        # patch work
        for dep in depas: ax.add_patch(dep)
        vertices = np.concatenate([dep.get_path().vertices for dep in depas])
        codes = np.concatenate([dep.get_path().codes for dep in depas])

        # clipper
        im.set_clip_path(PathPatch(Path(vertices, codes), transform=ax.transData))

    # other locate options
    if not loc:
        # country names 
        places = {'MEX':['mexico', 0.16, 0.65, 'México'], 
                    'BLZ':['belice', 0.85, 0.70, 'Belice'],
                    'SLV':['elsalvador', 0.65, 0.07, 'El Salvador'], 
                    'HND':['honduras', 0.86, 0.28, 'Honduras']}
        for place in places.values():
            print_names(place, ax)

        # ocean names
        oceans = [['pacifico', 0.14, 0.05, 'OCÉANO PACÍFICO'],
                    ['caribe', 0.88, 0.57, 'MAR CARIBE']]
        for ocean in oceans:
            print_names(ocean, ax, color='steelblue')

        # diferendo note
        props = dict(boxstyle='round', facecolor=mapgray, alpha=1, lw=0.2)
        plt.text(-88.90, 17.1, 'Diferendo\nterritorial,\ninsular y\nmarítimo\npendiente\nde resolver.',
                    color='#525252', va='bottom', ha='left', ma='center',
                    fontstyle='italic', fontvariant='normal', zorder=8, fontsize=3.3,
                    backgroundcolor=mapgray, rotation='horizontal', bbox=props)

    elif isinstance(loc, (str, list)):
        # place names
        if isinstance(loc, str):
            # prints main towns in region
            places = pp.regions[loc]
            for place in places.values():
                plot_points(place, ax)

        # draw municipalities if local map
        if loc!='CA':
            # draw shapes
            # municipalities
            plot_shapes(os.path.join(path_mapas, "muni/Municipios_340_dd.shp"), ax,
                        color='xkcd:charcoal', lw=0.5, ls='dashdot', zorder=2)

    ###########################################################################
    # texts, logos and foot of image

    # set title
    plt.title(title, color='black', size=11)

    # logo # inside map box
    if logoinmap:
        # read image # transparent
        logoim = image.imread(os.path.join(utilitiespath, 'logos', 'logo_INSIVUMEH.png'))

        # logo side length
        divisor = 2 if loc and loc!='CA' else 1
        logosl = (xlocator[1]-xlocator[0])/divisor
        # extent left-right
        if loc:
            exleft = lonmin+(lonmax-lonmin)*0.02
            exright = exleft+logosl
        else:
            exright = lonmax-(lonmax-lonmin)*0.02
            exleft = exright-logosl
        # extent top-down
        exbottom = latmin+(latmax-latmin)*0.02
        extop = exbottom+logosl

        # add image
        ax.imshow(logoim, aspect='equal', extent=(exleft, exright, exbottom, extop),
                    alpha=0.5, zorder=10)

    # foot # outside map box
    if foottext:
        # section text
        lt0 = 'Departamento de Investigación y Servicios Meteorológicos\n'
        lt1 = section
        lt2 = datafromtxt
        # auto insert newline
        lt0 = lt0 if lt0.endswith('\n') else lt0+'\n'
        lt1 = lt1 if lt1.endswith('\n') else lt1+'\n'
        lt2 = lt2 if lt2.endswith('\n') else lt2+'\n'
        # concat section lines
        ltc = lt0+lt1+lt2
        plt.text(0.30, -0.075, ltc, fontsize=5, transform=ax.transAxes, color='dimgray',
                    va="top", ha="left", multialignment="left")

        # info text
        plt.text(0.30, -0.15, infot, fontsize=5, transform=ax.transAxes, color=infocolor,
                    va="top", ha="left", multialignment="left")

        # logo outside map box
        if logo:
            # read image # transparent
            logoim = image.imread(os.path.join(utilitiespath, 'logos', 'logo_INSIVUMEH.png'))
            # put it in an offset box
            logobox = offsetbox.OffsetImage(logoim, zoom=0.04)
            # arbitrary offset
            logobox.set_offset((300, 40))
            ax.add_artist(logobox)

    # show figure
    if show:
        plt.show()

    # Save figure
    plt.savefig(os.path.join(outpath, figname), dpi=300, bbox_inches='tight', pad_inches=0.2)

    # old way to add logo outside map box with an external script
    # logo outside map box # external script
    # if logo:
    #     path_log = os.path.join(utilitiespath, 'logos/')
    #     pos_log = 'downsimple'
    #     logoscript = 'python3 {0} {1} {2} {1} {3}'.format(os.path.join(path_log, 'logo3.py'),
    #                                                 os.path.join(outpath, figname),
    #                                                 os.path.join(path_log, 'logochirpsmaps.png'),
    #                                                 pos_log)
    #     os.system(logoscript)

    plt.close('all')