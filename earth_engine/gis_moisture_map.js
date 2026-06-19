var nalgonda = ee.Geometry.Point([79.2671,17.0575]);

var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')

.filterBounds(nalgonda)

.filterDate('2025-01-01','2025-03-31')

.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))

.median();

// NDWI

var ndwi = s2.normalizedDifference(

['B3','B8']

).rename('NDWI');

// Moisture Stress

var stress = ndwi.expression(

'ndwi<-0.6 ? 3 : ndwi<-0.3 ? 2 : 1',

{

ndwi:ndwi

}

);

// Colors

Map.centerObject(nalgonda,10);

Map.addLayer(

stress,

{

min:1,

max:3,

palette:[

'green',

'yellow',

'red'

]

},

'Moisture Stress'

);
