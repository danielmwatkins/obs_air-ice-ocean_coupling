"""Helper functions for drifting buoy analysis and trajectory quality control
by Daniel Watkins. 

Functions defined here:
check_positions = check for invalid lat/lon and duplicated positions
check_dates = check for duplicated or reversed times
check_gaps = check length of segments, single points and short bursts are flagged
check_speed = checks u, v for outliers
standard_qc = wrapper for QC functions
interpolate_buoy_tracks = tool to interpolate buoy positions that masks places where
the interpolator tries to fill too large of gaps. Interpolation is done in stereographic
space rather than in lat/lon space.

compute_strain_rate_components = implementation of the deformation calculations of hutchings et al., 2012, 2018.
TBD for strain rates: dierking et al. uncertainty propagation, checks on whether the buoy arrays stretch too much or invert
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import pyproj

#### Function definitions
def check_positions(buoy_df, pairs_only=False,
                   latname='latitude', lonname='longitude'):
    """Looks for duplicated or nonphysical position data. Defaults to masking any 
    data with exact matches in latitude or longitude. Setting pairs_only to false 
    restricts the check to only flag where both longitude and latitude are repeated
    as a pair.
    """

    lats = buoy_df[latname].round(10)
    lons = buoy_df[lonname].round(10)
    
    invalid_lats = np.abs(lats) > 90
    if np.any(lons < 0):
        invalid_lons = np.abs(lons) > 180
    else:
        invalid_lons = lons > 360
        
    invalid = invalid_lats | invalid_lons
    
    repeated = lats.duplicated(keep='first') | lons.duplicated(keep='first')
    
    duplicated = pd.Series([(x, y) for x, y in zip(lons, lats)],
                                  index=buoy_df.index).duplicated(keep='first')
    
    if pairs_only:
        return duplicated | invalid
    
    else:
         return repeated | duplicated | invalid


def check_dates(buoy_df, precision='1min', date_col=None):
    """Check if there are reversals in the time or duplicated dates. Optional: check
    whether data are isolated in time based on specified search windows and the threshold
    for the number of buoys within the search windows. Dates are rounded to <precision>,
    so in some cases separate readings that are very close in time will be flagged
    as duplicates. Assumes date_col is in a format readable by pandas to_datetime.
    """

    if date_col is None:
        date_values = buoy_df.index.values
        date = pd.Series(pd.to_datetime(date_values).round(precision),
                     index=buoy_df.index)
    else:
        date = pd.to_datetime(buoy_df[date_col]).round(precision)
    duplicated_times = date.duplicated(keep='first')
    
    time_till_next = date.shift(-1) - date
    time_since_last = date - date.shift(1)

    negative_timestep = time_since_last.dt.total_seconds() < 0

    return negative_timestep | duplicated_times
    

def check_gaps(buoy_df, threshold_gap='4H', threshold_segment=12, date_col=None):
    """Segments the data based on a threshold of <threshold_gap>. Segments shorter
    than <threshold_segment> are flagged."""
    
    if date_col is None:
        date_values = buoy_df.index.values
        date = pd.Series(pd.to_datetime(date_values),
                     index=buoy_df.index)
    else:
        date = pd.to_datetime(buoy_df[date_col])
    
    time_till_next = date.shift(-1) - date
    segment = pd.Series(0, index=buoy_df.index)
    counter = 0
    tg = pd.to_timedelta(threshold_gap)
    for t in segment.index:
        segment.loc[t] = counter
        if time_till_next[t] > tg:
            counter += 1
    
    # apply_filter
    new = buoy_df.groupby(segment).filter(lambda x: len(x) > threshold_segment).index
    flag = pd.Series(True, index=buoy_df.index)
    flag.loc[new] = False
    return flag


def compute_velocity(buoy_df, date_index=True, rotate_uv=False, method='c', xvar='x', yvar='y'):
    """Computes buoy velocity and (optional) rotates into north and east directions.
    If x and y are not in the columns, projects lat/lon onto stereographic x/y prior
    to calculating velocity. Rotate_uv moves the velocity into east/west. Velocity
    calculations are done on the provided time index. Results will not necessarily 
    be reliable if the time index is irregular. With centered differences, values
    near endpoints are calculated as forward or backward differences.
    
    Options for method
    forward (f): forward difference, one time step
    backward (b): backward difference, one time step
    centered (c): 3-point centered difference
    forward_backward (fb): minimum of the forward and backward differences
    """
    buoy_df = buoy_df.copy()
    
    if date_index:
        date = pd.Series(pd.to_datetime(buoy_df.index.values), index=pd.to_datetime(buoy_df.index))
    else:
        date = pd.to_datetime(buoy_df.date)
        
    delta_t_next = date.shift(-1) - date
    delta_t_prior = date - date.shift(1)
    min_dt = pd.DataFrame({'dtp': delta_t_prior, 'dtn': delta_t_next}).min(axis=1)

    # bwd endpoint means the next expected obs is missing: last data before gap
    bwd_endpoint = (delta_t_prior < delta_t_next) & (np.abs(delta_t_prior - delta_t_next) > 2*min_dt)
    fwd_endpoint = (delta_t_prior > delta_t_next) & (np.abs(delta_t_prior - delta_t_next) > 2*min_dt)
    
    if xvar not in buoy_df.columns:
        projIn = 'epsg:4326' # WGS 84 Ellipsoid
        projOut = 'epsg:3413' # NSIDC North Polar Stereographic
        transformer = pyproj.Transformer.from_crs(projIn, projOut, always_xy=True)

        lon = buoy_df.longitude.values
        lat = buoy_df.latitude.values

        x, y = transformer.transform(lon, lat)
        buoy_df[xvar] = x
        buoy_df[yvar] = y
    
    if method in ['f', 'forward']:
        dt = (date.shift(-1) - date).dt.total_seconds().values
        dxdt = (buoy_df[xvar].shift(-1) - buoy_df[xvar])/dt
        dydt = (buoy_df[yvar].shift(-1) - buoy_df[yvar])/dt

    elif method in ['b', 'backward']:
        dt = (date - date.shift(1)).dt.total_seconds()
        dxdt = (buoy_df[xvar] - buoy_df[xvar].shift(1))/dt
        dydt = (buoy_df[yvar] - buoy_df[yvar].shift(1))/dt

    elif method in ['c', 'fb', 'centered', 'forward_backward']:
        fwd_df = compute_velocity(buoy_df.copy(), date_index=date_index, method='forward')
        bwd_df = compute_velocity(buoy_df.copy(), date_index=date_index, method='backward')

        fwd_dxdt, fwd_dydt = fwd_df['u'], fwd_df['v']
        bwd_dxdt, bwd_dydt = bwd_df['u'], bwd_df['v']
        
        if method in ['c', 'centered']:
            dt = (date.shift(-1) - date.shift(1)).dt.total_seconds()
            dxdt = (buoy_df[xvar].shift(-1) - buoy_df[xvar].shift(1))/dt
            dydt = (buoy_df[yvar].shift(-1) - buoy_df[yvar].shift(1))/dt
        else:
            dxdt = np.sign(bwd_dxdt)*np.abs(pd.DataFrame({'f': fwd_dxdt, 'b':bwd_dxdt})).min(axis=1)
            dydt = np.sign(bwd_dxdt)*np.abs(pd.DataFrame({'f': fwd_dydt, 'b':bwd_dydt})).min(axis=1)

        dxdt.loc[fwd_endpoint] = fwd_dxdt.loc[fwd_endpoint]
        dxdt.loc[bwd_endpoint] = bwd_dxdt.loc[bwd_endpoint]
        dydt.loc[fwd_endpoint] = fwd_dydt.loc[fwd_endpoint]
        dydt.loc[bwd_endpoint] = bwd_dydt.loc[bwd_endpoint]
    
    if rotate_uv:
        # Unit vectors
        buoy_df['Nx'] = 1/np.sqrt(buoy_df[xvar]**2 + buoy_df[yvar]**2) * -buoy_df[xvar]
        buoy_df['Ny'] = 1/np.sqrt(buoy_df[xvar]**2 + buoy_df[yvar]**2) * -buoy_df[yvar]
        buoy_df['Ex'] = 1/np.sqrt(buoy_df[xvar]**2 + buoy_df[yvar]**2) * -buoy_df[yvar]
        buoy_df['Ey'] = 1/np.sqrt(buoy_df[xvar]**2 + buoy_df[yvar]**2) * buoy_df[xvar]

        buoy_df['u'] = buoy_df['Ex'] * dxdt + buoy_df['Ey'] * dydt
        buoy_df['v'] = buoy_df['Nx'] * dxdt + buoy_df['Ny'] * dydt

        # Calculate angle, then change to 360
        heading = np.degrees(np.angle(buoy_df.u.values + 1j*buoy_df.v.values))
        heading = (heading + 360) % 360
        
        # Shift to direction from north instead of direction from east
        heading = 90 - heading
        heading = (heading + 360) % 360
        buoy_df['bearing'] = heading
        buoy_df['speed'] = np.sqrt(buoy_df['u']**2 + buoy_df['v']**2)
        buoy_df.drop(['Nx', 'Ny', 'Ex', 'Ey'], axis=1, inplace=True)
        
    else:
        buoy_df['u'] = dxdt
        buoy_df['v'] = dydt            
        buoy_df['speed'] = np.sqrt(buoy_df['v']**2 + buoy_df['u']**2)    

    return buoy_df

def check_speed(buoy_df, date_index=True, window='3D', sigma=5, max_speed=1.5):
    """If the position of a point is randomly offset from the path, there will
    be a signature in the velocity. The size of the anomaly will differ depending
    on the time resolution. 
    
    Update to check sequentially, or to update if something is masked.
    
    window can be either time or integer, it is passed to the pandas rolling
    method for calculating anomalies. Default is to use 24 observations for the calculations.
    Data near endpoints are compared to 
    
    method will have more options eventually, for now just z score.
    
    In this method, I first calculate a Z-score for the u and v velocity components, using the 
    forward-backward difference method. This method calculates velocity with forward differences and
    with backward differences, and returns the value with the smallest magnitude. It is therefore
    designed to catch when there is a single out-of-place point. Z-scores are calcuted by first 
    removing the mean over a centered period with the given window size (default 3 days), then
    dividing by the standard deviation over the same period. The Z-scores are then detrended by
    subtracting the median over the same window. When a data point has a Z-score larger than 3, the 
    nearby Z-scores are recalculated with that value masked. Finally, Z-scores larger than 6 are masked.
    """

    buoy_df = buoy_df.copy()
    if date_index:
        date = pd.Series(pd.to_datetime(buoy_df.index.values).round('1min'), index=pd.to_datetime(buoy_df.index))
    else:
        date = pd.to_datetime(buoy_df.date).round('1min')

    window = pd.to_timedelta(window)
    
    n_min = 0.4*buoy_df.rolling(window, center=True).count()['latitude'].median()

    if n_min > 0:
        n_min = int(n_min)
    else:
        print('n_min is', n_min, ', setting it to 10.')
        n_min = 10
        
    def zscore(df, window, n_min):
        uscore = (df['u'] - df['u'].rolling(window, center=True, min_periods=n_min).mean()) / \
                 df['u'].rolling(window, center=True, min_periods=n_min).std()
        vscore = (df['v'] - df['v'].rolling(window, center=True, min_periods=n_min).mean()) / \
                 df['v'].rolling(window, center=True, min_periods=n_min).std()

        zu_anom = uscore - uscore.rolling(window, center=True, min_periods=n_min).median()
        zv_anom = vscore - vscore.rolling(window, center=True, min_periods=n_min).median()
        
        return zu_anom, zv_anom

    # First calculate speed using backward difference and get Z-score
    df = compute_velocity(buoy_df, date_index=True, method='fb')

    zu_init, zv_init = zscore(df, window, n_min)
    zu, zv = zscore(df, window, n_min)

    # Anytime the Z score for U or V velocity is larger than 3, re-calculate Z
    # scores leaving that value out.
    # Probably should replace with a while loop so that it can iterate a few times
    for date in df.index:
        if (np.abs(zu[date]) > 3) | (np.abs(zv[date]) > 3):
            # Select part of the data frame that is 2*n_min larger than the window
            idx = df.index[np.abs(df.index - date) < (1.5*window)].drop(date)
            df_new = compute_velocity(df.drop(date).loc[idx,:], method='fb')
            zu_idx, zv_idx = zscore(df_new, window, n_min)

            idx = zu_idx.index[np.abs(zu_idx.index - date) < (0.5*window)]
            zu.loc[idx] = zu_idx.loc[idx]
            zv.loc[idx] = zv_idx.loc[idx]

    flag = df.u.notnull() & ((np.abs(zu) > sigma) | (np.abs(zv) > sigma))
    df = compute_velocity(buoy_df.loc[~flag], method='fb')
    if np.any(df.speed > max_speed):
        flag = flag | (df.speed > max_speed)

    return flag


#### Define QC algorithm ####
def standard_qc(buoy_df,
                min_size=100,
                gap_threshold='6H',                
                segment_length=24,
                lon_range=(-180, 180),
                lat_range=(65, 90),
                max_speed=1.5,
                speed_window='3D',
                verbose=False):
    """QC steps applied to all buoy data. Wrapper for functions in drifter.clean package.
    min_size = minimum number of observations
    gap_threshold = size of gap between observations that triggers segment length check
    segment_length = minimum size of segment to include
    lon_range = tuple with (min, max) longitudes
    lat_range = tuple with (min, max) latitudes
    verbose = if True, print messages to see where data size is reduced
    
    Algorithm
    1. Check for duplicated and reversed dates with check_dates()
    2. Check for duplicated positions with check_positions() with pairs_only set to True.
    3. Check for gaps and too-short segments using check_gaps()
    4. Check for anomalous speeds using check_speed()
    """
    buoy_df_init = buoy_df.copy()
    n = len(buoy_df)
    flag_date = check_dates(buoy_df)
    flag_pos = check_positions(buoy_df, pairs_only=True)
    buoy_df = buoy_df.loc[~(flag_date | flag_pos)].copy()
    if verbose:
        if len(buoy_df) < n:
            print('Initial size', n, 'reduced to', len(buoy_df))

    def bbox_select(df):
        """Restricts the dataframe to data within
        the specified lat/lon ranges. Selects data from the earliest
        day that the data is in the range to the last day the data
        is in the range. In between, the buoy is allowed to leave
        the bounding box."""
        lon = df.longitude
        lat = df.latitude
        lon_idx = (lon > lon_range[0]) & (lon < lon_range[1])
        lat_idx = (lat > lat_range[0]) & (lat < lat_range[1])
        idx = df.loc[lon_idx & lat_idx].index
        return df.loc[(df.index >= idx[0]) & (df.index <= idx[-1])].copy()
        
    buoy_df = bbox_select(buoy_df)

    if verbose:
        if len(buoy_df) < n:
            print('Initial size', n, 'reduced to', len(buoy_df))
    
    # Return None if there's insufficient data
    if len(buoy_df) < min_size:
        print('Observations in bounding box', n, 'less than min size', min_size)
        return None

    flag_gaps = check_gaps(buoy_df,
                           threshold_gap=gap_threshold,
                           threshold_segment=segment_length)
    buoy_df = buoy_df.loc[~flag_gaps].copy()
    
    
    
    # Check speed
    flag_speed = check_speed(buoy_df, window=speed_window, max_speed=max_speed)
    buoy_df = buoy_df.loc[~flag_speed].copy()

    if len(buoy_df) < min_size:
        return None
    
    else:
        buoy_df_init['flag'] = True
        buoy_df_init.loc[buoy_df.index, 'flag'] = False
        return buoy_df_init

# Interpolate to a regular grid
def interpolate_buoy_track(buoy_df, xvar='longitude', yvar='latitude', 
                           freq='1H', maxgap_minutes=240):
    """Applies interp1d with cubic splines to the pair of variables specied by
    xvar and yvar. Assumes that the dataframe buoy_df has a datetime index.
    Frequency should be in a form understandable to pandas date_range, e.g. '1H' for hourly.
    """

    buoy_df = buoy_df.dropna(subset=[xvar, yvar]).copy()

    # if x/y are longitude/latitude or lat/lon,
    # project to north polar stereographic first.
    if (xvar == 'longitude') | (xvar == 'lon'):
        reproject = True
        projIn = 'epsg:4326' # WGS 84 Ellipsoid
        projOut = 'epsg:3413' # NSIDC Polar Stereographic
        transform_to_xy = pyproj.Transformer.from_crs(
            projIn, projOut, always_xy=True)
        transform_to_ll = pyproj.Transformer.from_crs(
            projOut, projIn, always_xy=True)

        lon = buoy_df.longitude.values
        lat = buoy_df.latitude.values

        xvar = 'x_stere'
        yvar = 'y_stere'

        x, y = transform_to_xy.transform(lon, lat)
        buoy_df[xvar] = x
        buoy_df[yvar] = y
    else:
        reproject = False
    
    t = pd.Series(buoy_df.index)
    dt = pd.to_timedelta(t - t.min()).dt.total_seconds()
    tnew = pd.date_range(start=t.min().round(freq), end=t.max().round(freq), freq=freq).round(freq)
    dtnew = pd.to_timedelta(tnew - t.min()).total_seconds()
    
    X = buoy_df[[xvar, yvar]].T
    time_till_next = t.shift(-1) - t
    time_since_last = t - t.shift(1)

    time_till_next = time_till_next.dt.total_seconds()
    time_since_last = time_since_last.dt.total_seconds()

    Xnew = interp1d(dt, X.values, bounds_error=False, kind='cubic')(dtnew).T

    # add information on initial time resolution 
    data_gap = interp1d(dt, np.sum(np.array([time_till_next.fillna(0),
                                             time_since_last.fillna(0)]), axis=0),
                  kind='previous', bounds_error=False)(dtnew)

    df_new = pd.DataFrame(data=np.round(Xnew, 5), 
                          columns=[xvar, yvar],
                          index=tnew)
    df_new.index.names = ['datetime']
    
    df_new['data_gap_minutes'] = np.round(data_gap/60)/2 # convert from sum to average gap at point
    df_new = df_new.where(df_new.data_gap_minutes < maxgap_minutes).dropna()
    
    if reproject:
        x = df_new[xvar].values
        y = df_new[yvar].values

        lon, lat = transform_to_ll.transform(x, y)
        df_new['longitude'] = np.round(lon, 5)
        df_new['latitude'] = np.round(lat, 5)

    return df_new




def compute_strain_rate_components(buoys, data, position_uncertainty, time_delta='1H'):
    """Compute the four components of strain rate for each
    date in data. Assumes velocity has already been calculated.
    Expects "data" to be a dictionary with a dataframe for each
    of the buoys in the list "buoys". The dataframes in "data"
    should have columns "u", "v", "longitude", "latitude". Buoys should
    be listed so that the polygon linking them is in counterclockwise order.

    Output: dataframe with columns 'divergence', 'vorticity',
             'pure_shear', 'normal_shear', 'maximum_shear_strain_rate',
             'area', 'shape_flag'

    Position uncertainty is expected to be in standard deviation form, so
    the units should be meters.

    Time delta is the length of time used in the calculation of velocity. Needs to be in
    format understandable by pandas to_timedelta(), e.g. '1H' for one hour.
    """

    def polygon_area(X, Y):
        """Compute area of polygon as a sum. Should use LAEA not PS here"""
        sumvar = 0.
        N = len(X)        
        for i in range(N):
            sumvar += X[i]*Y[(i+1) % N] - Y[i]*X[(i+1) % N]
        return sumvar*0.5

    def polygon_area_uncertainty(X, Y, position_uncertainty):
        """Compute the area uncertainty following Dierking et al. 2020"""
        N = len(X)
        S = 0
        for i in range(N):
            # the modulus here makes the calculation wrap around to the beginning
            # could adjust the other codes to do this too
            S += (X[(i+1) % N] - X[(i-1) % N])**2 +  (Y[(i+1) % N] - Y[(i-1) % N])**2
        return np.sqrt(0.25*position_uncertainty**2*S)

    def gradvel_uncertainty(X, Y, U, V, A, position_uncertainty, time_delta, vel_var='u', x_var='x'):
        """Equation 19 from Dierking et al. 2020 assuming uncertainty in position is same in both x and y.
        Also assuming that there is no uncertainty in time. Default returns standard deviation
        uncertainty for dudx.
        """
        sigma_A = polygon_area_uncertainty(X, Y, position_uncertainty)
        sigma_X = position_uncertainty
        
        # velocity uncertainty
        if vel_var=='u':
            u = U.copy()
        else:
            u = V.copy()
        if x_var == 'x':
            # If you want dudx, integrate over Y
            x = Y.copy()
        else:
            x = X.copy()
        
        sigma_U = 2*sigma_X**2/time_delta**2
        
        
        N = len(X)
        S1, S2, S3 = 0, 0, 0
        for i in range(N):
            # the modulus here makes the calculation wrap around to the beginning
            # could adjust the other codes to do this too
            S1 += (u[(i+1) % N] + u[(i-1) % N])**2 * (x[(i+1) % N] - x[(i-1) % N])**2
            S2 += (x[(i+1) % N] - x[(i-1) % N])**2
            S3 += (u[(i+1) % N] + u[(i-1) % N])**2
            
        var_ux = sigma_A**2/(4*A**4)*S1 + \
                 sigma_U**2/(4*A**2)*S2 + \
                 sigma_X**2/(4*A**2)*S3       
        
        return np.sqrt(var_ux)

    
    def accel(X, U, A, sign):
        """Computes spatial derivative of velocity for 
        deformation."""
        N = len(X)
        sumvar = 0
        for i in range(N):
            sumvar += (U[(i+1) % N] + U[i])*(X[(i+1) % N] - X[i])
        return 1/(2*A) * sumvar * sign

    lon_data = pd.DataFrame({b: data[b]['longitude'] for b in buoys})
    lat_data = pd.DataFrame({b: data[b]['latitude'] for b in buoys})
    time_delta = pd.to_timedelta(time_delta).total_seconds()
    
    # Polar stereographic for velocity-based component
    projIn = 'epsg:4326' # WGS 84 Ellipsoid
    projOut = 'epsg:3413' # NSIDC North Polar Stereographic
    transformer_ps = pyproj.Transformer.from_crs(projIn, projOut, always_xy=True)

    projOut = 'epsg:6931' # NSIDC EASE 2.0 (for area calculation)
    transformer_laea = pyproj.Transformer.from_crs(projIn, projOut, always_xy=True)
    
    X_data = lon_data * np.nan
    Y_data = lon_data * np.nan
    XA_data = lon_data * np.nan
    YA_data = lon_data * np.nan
    U_data = lon_data * np.nan
    V_data = lon_data * np.nan    
    
    for buoy in X_data.columns:
        lon = lon_data[buoy].values
        lat = lat_data[buoy].values

        x, y = transformer_ps.transform(lon, lat)
        X_data[buoy] = x
        Y_data[buoy] = y
        
        xa, ya = transformer_laea.transform(lon, lat)
        XA_data[buoy] = xa
        YA_data[buoy] = ya
        
        buoy_df = pd.DataFrame({'longitude': lon,
                                'latitude': lat,
                                'x': x,
                                'y': y}, index=X_data.index)
        buoy_df = compute_velocity(buoy_df)
        U_data[buoy] = buoy_df['u']
        V_data[buoy] = buoy_df['v']
    
    X = X_data.T.values
    Y = Y_data.T.values
    XA = XA_data.T.values
    YA = YA_data.T.values        
    U = U_data.T.values
    V = V_data.T.values

    A = polygon_area(XA, YA)

    # Check order of points
    # Can't handle reversal partway through though
    if np.all(A[~np.isnan(A)] < 0):
        print('Reversing order')
        X = X[::-1,:]
        XA = XA[::-1,:]
        Y = Y[::-1,:]
        YA = YA[::-1,:]
        U = U[::-1,:]
        V = V[::-1,:]
        
    A = polygon_area(XA, YA)

    dudx = accel(Y, U, A, 1)
    dudy = accel(X, U, A, -1)
    dvdx = accel(Y, V, A, 1)
    dvdy = accel(X, V, A, -1)

    divergence = dudx + dvdy
    vorticity = dvdx - dudy
    pure_shear = dudy + dvdx
    normal_shear = dudx - dvdy
    maximum_shear_strain_rate = np.sqrt(pure_shear**2 + normal_shear**2)
    total_deformation = np.sqrt(divergence**2 + maximum_shear_strain_rate**2)


    sigma_A = polygon_area_uncertainty(X, Y, position_uncertainty)
    sigma_dudx = gradvel_uncertainty(X, Y, U, V, A,
                                     position_uncertainty, time_delta, vel_var='u', x_var='x')
    sigma_dvdx = gradvel_uncertainty(X, Y, U, V, A,
                                     position_uncertainty, time_delta, vel_var='v', x_var='x')
    sigma_dudy = gradvel_uncertainty(X, Y, U, V, A,
                                     position_uncertainty, time_delta, vel_var='u', x_var='y')
    sigma_dvdy = gradvel_uncertainty(X, Y, U, V, A,
                                     position_uncertainty, time_delta, vel_var='v', x_var='y')

    sigma_div = np.sqrt(sigma_dudx**2 + sigma_dvdy**2)
    sigma_vrt = np.sqrt(sigma_dvdx**2 + sigma_dudy**2)
    sigma_shr = np.sqrt((normal_shear/maximum_shear_strain_rate)**2 * (sigma_dudx**2 + sigma_dvdy**2) + \
                        (pure_shear/maximum_shear_strain_rate)**2 * (sigma_dudy**2 + sigma_dvdx**2))
    sigma_tot = np.sqrt((maximum_shear_strain_rate/total_deformation)**2 * sigma_shr**2 + \
                        (divergence/total_deformation)**2 * sigma_vrt**2)
        
    results_df = pd.DataFrame(
        {'divergence': divergence,
         'vorticity': vorticity,
         'pure_shear': pure_shear,
         'normal_shear': normal_shear,
         'maximum_shear_strain_rate': maximum_shear_strain_rate,
         'total_deformation': total_deformation,
         'area': A,
         'uncertainty_area': sigma_A,
         'uncertainty_divergence': sigma_div,
         'uncertainty_vorticity': sigma_vrt,
         'uncertainty_shear': sigma_shr,
         'uncertainty_total': sigma_tot,
         'shape_flag': np.sign(A)},
        index=X_data.index)
    
    return results_df
def regrid_buoy_track(buoy_df, precision='5min'):
    """Applies interp1d with cubic splines to align the buoy track to a 5 min grid.
    Assumes that the dataframe buoy_df has a datetime index. Errors are reported by
    computing the difference between the interpolating curve and the original
    data points, then linearly interpolating the error to the new grid. 
    Calculations carried out in north polar stereographic coordinates.
    """

    projIn = 'epsg:4326' # WGS 84 Ellipsoid
    projOut = 'epsg:3413' # NSIDC Polar Stereographic
    transform_to_xy = pyproj.Transformer.from_crs(projIn, projOut, always_xy=True)
    transform_to_ll = pyproj.Transformer.from_crs(projOut, projIn, always_xy=True)
    
    lon = buoy_df.longitude.values
    lat = buoy_df.latitude.values
    
    xvar = 'x_stere'
    yvar = 'y_stere'
    
    x, y = transform_to_xy.transform(lon, lat)
    buoy_df[xvar] = x
    buoy_df[yvar] = y


    t = pd.Series(buoy_df.index)
    t0 = t.min()
    t_seconds = pd.to_timedelta(t - t0).dt.total_seconds()

    tnew = t.round(precision)
     # Drop data points that are closer than <precision> to each other
    tnew = tnew.loc[~tnew.duplicated()]
    
    tnew_seconds = pd.to_timedelta(tnew - t0).dt.total_seconds()

    X = buoy_df[[xvar, yvar]].T.values
    Xnew = interp1d(t_seconds, X, bounds_error=False, kind='cubic')(tnew_seconds)
    idx = ~np.isnan(Xnew.sum(axis=0))
    buoy_df_new = pd.DataFrame(data=np.round(Xnew.T, 5), 
                          columns=[xvar, yvar],
                          index=tnew)
    buoy_df_new.index.names = ['datetime']

    # Next, get the absolute position error
    Xnew_at_old = interp1d(
        tnew_seconds[idx], Xnew[:, idx],
        bounds_error=False, kind='cubic')(t_seconds)
    X_err = pd.Series(
        np.sqrt(np.sum((X - Xnew_at_old)**2, axis=0)), t).ffill().bfill()

    # Finally, assign absolute position error to the new dataframe
    buoy_df_new['sigma_x_regrid'] = interp1d(t_seconds, X_err,
                                             bounds_error=False,
                                             kind='nearest')(tnew_seconds)

    x = buoy_df_new[xvar].values
    y = buoy_df_new[yvar].values

    lon, lat = transform_to_ll.transform(x, y)
    buoy_df_new['longitude'] = lon
    buoy_df_new['latitude'] = lat

    return buoy_df_new