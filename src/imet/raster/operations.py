import xarray as xr

def mean(data: xr.DataArray, skipna: bool = False):
	return xr.DataArray.mean(data, dim=0, skipna=skipna)

def sum(data: xr.DataArray, skipna: bool = False):
	return xr.DataArray.sum(data, dim=0, skipna=skipna)

def max(data: xr.DataArray, skipna: bool = False):
	return xr.DataArray.max(data, dim=0, skipna=skipna)

def min(data: xr.DataArray, skipna: bool = False):
	return xr.DataArray.min(data, dim=0, skipna=skipna)

def quantile(data: xr.DataArray, quantile: float, skipna: bool = False):
	return xr.DataArray.quantile(data, q=quantile, dim=0, skipna=skipna)
