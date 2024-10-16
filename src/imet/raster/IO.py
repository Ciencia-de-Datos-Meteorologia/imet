import os
import numpy as np
import pandas as pd
import xarray as xr
import rioxarray as rio
#
from typing import Union, List

def read_file(files: Union[str, List[str]], path: str = ''):
    """
    Read data file. Interprets file format.
    """

    # TIF files
    if files.lower().endswith(('.tif', '.tiff')):
        data = read_tif(files, path)

    return data

def read_tif(files: Union[str, List[str]], path: str = '',
                x: str = 'x', y: str = 'y'):
    """
    Read data from TIFF (Tag Image File Format) files.

    Parameters
    ----------
        files: str or list[str]
            File name or list of files.
        path: str, default None
            Path to file. Optional.
        x: str, default 'x'
            Name of the x dimension.
        y: str, default 'y'
            Name of the y dimension.

    Returns
    -------
        xarray.DataArray
            Data read from file or concatenated data read from multiple files.
    
    Raises
    ------
        ValueError
            If coordinates do not match when reading multiple files.
    """

    # read singular TIFF file
    if isinstance(files, str):
        # load data from file
        data = rio.open_rasterio(os.path.join(path, files))

        # get only the first band
        data = data.isel(band=0, drop=True)

        # remake DataArray object
        # this drops other dimensions and attributes
        data = xr.DataArray(data.data,
                            dims=[y, x],
                            coords=[data[y], data[x]])

    # read list of TIFF files
    elif isinstance(files, list):
        # lists to store data and file names
        data_list = []
        file_list = []

        # iterate over file list
        for ifile in files:
            # read TIFF file
            # recursively calls this function
            fdata = read_tif(ifile, path)

            # save new data to lists
            data_list.append(fdata)
            file_list.append(os.path.splitext(os.path.basename(ifile))[0])

        # create a single DataArray, by concatenating list of DataArrays
        if len(data_list)>1:
            # try fails if coordinates are not equal in all files
            try:
                # concat DataArrays, along a new 'source' dimension
                #   joining 'exact' raises an error if coordinates are
                #   different across files
                data = xr.concat(data_list,
                                    dim=pd.Index(file_list, name='source'),
                                    join='exact')
            except:
                raise ValueError("Coordinates DO NOT match")
        # otherwise list only had 1 file
        else:
            data = data_list[0]

    return data










