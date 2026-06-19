var nalgonda = ee.Geometry.Point([79.2671,17.0575]);

var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')

.filterBounds(nalgonda)

.filterDate('2025-01-01','2025-03-31')

.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))

.median();

var ndvi = s2.normalizedDifference(

['B8','B4']

).rename('NDVI');

Map.centerObject(nalgonda,10);

Map.addLayer(

ndvi,

{

min:0,

max:1,

palette:[

'red',

'yellow',

'green'

]

},

'NDVI'

);
