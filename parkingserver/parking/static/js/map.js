var platform = new H.service.Platform({
  'app_id': 'drIAftNO5tvoGsybyT7K',
  'app_code': 'FxNZb7kWTb_vKdzoeDS1-Q'
});
lat=0;
lng=0;

var icon1 = new H.map.Icon("/static/img/parkings.png");
var icon2 = new H.map.Icon("/static/img/parkingUDs.png");
var icon3 = new H.map.Icon("/static/img/parkingfar.png");
var icon4 = new H.map.Icon("/static/img/parkinglock.png");

var maptypes = platform.createDefaultLayers();
var my = new H.map.Group;
var parkings = new H.map.Group;
var map = new H.Map(
document.getElementById('map'),
maptypes.normal.map,
{
zoom: 10,
center: { lng: 13.4, lat: 52.51 }
});
map.addObject(parkings);
map.addObject(my);
var mapEvents = new H.mapevents.MapEvents(map);
var behavior = new H.mapevents.Behavior(mapEvents);
map.addEventListener('tap', function(evt) {
console.log(evt.type, evt.currentPointer.type); 
});
$(document).ready(function(){locateme();});

function locateme(){
    my.removeAll();
    navigator.geolocation.getCurrentPosition(function(location) {
    lat=location.coords.latitude;
    lng=location.coords.longitude;
    map.setCenter({lng:lng,lat:lat});
    map.setZoom(15);
    var thisPlaceMarker = new H.map.Marker({lat:lat, lng:lng});
    my.addObject(thisPlaceMarker);
    loadDataFromServer();
})
}

window.addEventListener('resize', function () {
  map.getViewPort().resize(); 
});

function loadDataFromServer(except){
  success=false;
  mylocation = new FormData;
  mylocation.append('csrfmiddlewaretoken', csrftoken);
  mylocation.append('lat',lat);
  mylocation.append('lng',lng);
  $.post({url:"/getdataparking",processData: false, contentType: false,data:mylocation,success:function(data){
    success = data.success;
    datafromserver.clear();
    if(success){
      if(except != null){
        exceptID = except.values_.data.id;
      }
      else
      {
        exceptID = null
      }
      for( parking in data.result){
        if(data.result[parking].id != exceptID){
          if(data.result[parking].on_use){
            addMarkerToGroup(parkings,data.result[parking],icon2);
            console.log('free');
          }
          else{
            addMarkerToGroup(parkings,data.result[parking],icon1);
            console.log('onuse');
          }
          
        }
        else{
          HL.clear();
        }
        }
        for( parking in data.far){
          if(data.far[parking].id != exceptID){
            addMarkerToGroup(parkings,data.far[parking],icon3);
          }
          else{
            HL.clear();
          }
        }
        for(parking in data.locked){
          if(data.locked[parking].id != exceptID){
            addMarkerToGroup(parkings,data.locked[parking],icon4);
          }
        }
    }        
}});
return success;
}


function addMarkerToGroup(group, inf,op) {
  var marker = new H.map.Marker({lat:inf.lat,lng:inf.lng});
  marker.setData(inf);
  marker.icon=op;
  //marker.icon();
  //marker.scale()
  group.addObject(marker);
}

map.addEventListener('tap', function (evt) {
  if(evt.target.P.hasOwnProperty("id")){
    console.log(evt.target.P);
    opencontentfeature(evt.target.P);
  }
  else{
    var coord = map.screenToGeo(evt.currentPointer.viewportX,
    evt.currentPointer.viewportY);
    lat=coord.lat;
    lng=coord.lng;
    contentdrawer.open=false;
    drawer.open=false;
    my.removeAll();
    var thisPlaceMarker = new H.map.Marker({lat:lat, lng:lng});
    my.addObject(thisPlaceMarker);
  }
}, false);

function opencontentfeature(feature){
 
  $.post("/parkingdetail",{'csrfmiddlewaretoken': csrftoken,'id':feature.id},function(data){
    $('#contentdrawer').css('width','500px')
    $('#secondarycontent').empty();
    $('#secondarycontent').append(data);
    contentdrawer.open=true;
  })
  
};

var scalevar=2;
var lat = null;
var lng = null;
var label = null;

//mediaquery equivalent on javascript
function myFunction(x) {
  if (x.matches) { // If media query matches
      scalevar=0.7;
  } else {
      scalevar=1;
  }
  console.log(scalevar);
}
  
var x = window.matchMedia("(max-width: 599px)")
myFunction(x) // Call listener function at run time
x.addListener(myFunction) // Attach listener function on state changes


//style definitions for features on map
function StyleGet(feature,texto){
  var styles = {
    'route': new ol.style.Style({
      stroke: new ol.style.Stroke({
        width: 6, color: [237, 212, 0, 0.8]
      })
    }),
    'icon': new ol.style.Style({
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: "/static/img/location2.png",
        scale:scalevar
      })
    }),
    'parking': new ol.style.Style({
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: "/static/img/parkings.png",
        scale:scalevar
      })
    }),
    'parking-on_use': new ol.style.Style({
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: "/static/img/parkingUDs.png",
        scale:scalevar
      })
    }),
    'parkingSELECT': new ol.style.Style({
      text: new ol.style.Text({
        text:texto,
        font: '22px Calibri,sans-serif',
        textAlign: 'center',
        offsetY: -110,
        fill: new ol.style.Fill({
          color: [255,255,255,1]
        }),
        stroke: new ol.style.Stroke({
          color: [0, 0, 0,1],
          width: 4
        })}),
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: "/static/img/parkingSEc.png",
        scale:scalevar
      })
    }),
    'parkingSELECT-lock': new ol.style.Style({
      text: new ol.style.Text({
        text:texto,
        font: '22px Calibri,sans-serif',
        textAlign: 'center',
        offsetY: -110,
        fill: new ol.style.Fill({
          color: [255,255,255,1]
        }),
        stroke: new ol.style.Stroke({
          color: [0, 0, 0,1],
          width: 4
        })}),
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: "/static/img/parkingSElock.png",
        scale:scalevar
      })
    }),
    'parkingSELECT-on_use': new ol.style.Style({
      text: new ol.style.Text({
        text:texto,
        font: '22px Calibri,sans-serif',
        textAlign: 'center',
        offsetY: -110,
        fill: new ol.style.Fill({
          color: [255,255,255,1]
        }),
        stroke: new ol.style.Stroke({
          color: [0, 0, 0,1],
          width: 4
        })}),
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: "/static/img/parkingUDSEc.png",
        scale:scalevar
      })
    }),
    'parking-far': new ol.style.Style({
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: "/static/img/parkingfar.png",
        scale:scalevar
      })
    }),
    'parking-lock': new ol.style.Style({
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: "/static/img/parkinglock.png",
        scale:scalevar
      })
    }),
    'parkingHL': new ol.style.Style({
      text: new ol.style.Text({
      text:texto,
      font: '14px Calibri,sans-serif',
      textAlign: 'center',
      offsetY: -70,
      fill: new ol.style.Fill({
        color: [0,0,0,1]
      }),
      stroke: new ol.style.Stroke({
        color: [255, 129, 11,0.5],
        width: 4
      })}),
      image: new ol.style.Icon({
        anchor: [0.5, 0.91],
        src: "/static/img/HL1.png",
        scale:scalevar
      })
    }),
    'parkingHL-far': new ol.style.Style({
      text: new ol.style.Text({
        text:texto,
        font: '14px Calibri,sans-serif',
        textAlign: 'center',
        offsetY: -50,
        fill: new ol.style.Fill({
          color: [0,0,0,1]
        }),
        stroke: new ol.style.Stroke({
          color: [255, 129, 11,0.5],
          width: 4
        })}),
      image: new ol.style.Icon({
        anchor: [0.5, 0.91],
        src: "/static/img/HL2.png",
        scale:scalevar
      })
    }),
    'parkingHL-lock': new ol.style.Style({
      text: new ol.style.Text({
        text:texto,
        font: '14px Calibri,sans-serif',
        textAlign: 'center',
        offsetY: -50,
        fill: new ol.style.Fill({
          color: [0,0,0,1]
        }),
        stroke: new ol.style.Stroke({
          color: [255, 129, 11,0.5],
          width: 4
        })}),
      image: new ol.style.Icon({
        anchor: [0.5, 0.93],
        src: "/static/img/HL3.png",
        scale:scalevar
      })
    }),
    'ghosticon': new ol.style.Style({
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: "/static/img/location2.png",
        scale:scalevar,
        opacity:0.5
      })
    }),
    'geoMarker': new ol.style.Style({
      image: new ol.style.Circle({
        radius: 7,
        fill: new ol.style.Fill({color: 'black'}),
        stroke: new ol.style.Stroke({
          color: 'white', width: 2
        })
      })
    }),
    'circleMarker': new ol.style.Style({
      fill: new ol.style.Fill({
        color: 'rgba(255, 100, 50, 0.3)'
    }),
    stroke: new ol.style.Stroke({
        width: 2,
        color: 'rgba(255, 100, 50, 0.8)'
    }),
    })
  };
  return styles[feature.get('type')]
}


//geo-location and map configuration
var here = new ol.proj.transform([-70.6492634,-33.4419814], 'EPSG:4326', 'EPSG:3857');
var point = new ol.geom.Point(here);
var circle = new ol.geom.Circle(here, 500);
var circleFeature = new ol.Feature({
  type:'circleMarker',
  geometry:circle
});

var initMarker = new ol.Feature({
  type:'icon',
  geometry: point
});

var datafromserver = new ol.source.Vector({
  projection: 'EPSG:4326',
  features: []
});

var HL = new ol.source.Vector({
  projection: 'EPSG:4326',
  features: []
});

var sourcedy = new ol.source.Vector({
  projection: 'EPSG:4326',
  features: []
});

var SELECTEDsource = new ol.source.Vector({
  projection: 'EPSG:4326',
  features: []
});

if (lastlat!=null && lastlng!=null){
  const there = new ol.proj.transform([lastlng,lastlat], 'EPSG:4326', 'EPSG:3857');
  const point0 = new ol.geom.Point(there);

  var lastMarker = new ol.Feature({
    type:'ghosticon',
    geometry: point0
  });

  sourcedy.addFeature(lastMarker);
}

var vectorLayer0 = new ol.layer.Vector({
  source:datafromserver,
  style:function(feature) {
    return StyleGet(feature,feature.get('etiqueta'));
  }
});

var vectorLayer1 = new ol.layer.Vector({
  source:HL,
  style:function(feature) {
    return StyleGet(feature,feature.get('etiqueta'));
  }
});

var vectorLayer = new ol.layer.Vector({
  source:sourcedy,
  style: function(feature) {
    return StyleGet(feature,feature.get('etiqueta'));
  }
});

var vectorLayerSE = new ol.layer.Vector({
  source:SELECTEDsource,
  style: function(feature) {
    return StyleGet(feature,feature.get('etiqueta'));
  }
});

//  var map = new ol.Map({
//    target: 'map',
//    layers: [
//      new ol.layer.Tile({
//        source: new ol.source.OSM()
//      }),
//      vectorLayer0,
//      vectorLayer1,
//      vectorLayer,
//      vectorLayerSE
//    ],
//    view: new ol.View({
//      center: here,
//      zoom: 11,
//      minZoom:5
//      
//    }),
//    controls : ol.control.defaults({
//      attribution : false,
//      zoom : false,
//    })
//  });

  
function findme(){
  navigator.geolocation.getCurrentPosition(function(location) {
    lat=location.coords.latitude;
    lng=location.coords.longitude;
    here = ol.proj.transform([lng,lat], 'EPSG:4326', 'EPSG:3857');
    point.setCoordinates(here);
    circle.setCenter(here);
    map.getView().animate({duration:1500, center:here, zoom:17});
    loadDataFromServer();
  });
}

function findSelected(){
  map.getView().animate({duration:1500, center:selectedFeature.getGeometry(), zoom:17});
}

function addBasicMarkers(){
  sourcedy.addFeature(initMarker);
  sourcedy.addFeature(circleFeature);
}

findme();
addBasicMarkers();
var selectedFeature = null;

map.on('click', function(evt){
  var punto=  ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326')
  selectedFeature = null;
  
  map.forEachFeatureAtPixel(evt.pixel, function (feature, layer) {
    selectedFeature = null;
    console.log(feature);
    if((feature.values_.type=="parking" || feature.values_.type=="parking-far" || feature.values_.type=="parking-on_use"|| feature.values_.type=="parking-lock") && map.getView().getZoom() >= 13){
      selectedFeature = feature;
      SELECTEDsource.clear();
      loadDataFromServer(feature);
      if(selectedFeature.values_.data.lock){
        SELECTEDsource.addFeature(new ol.Feature({
          type:'parkingSELECT-lock',
          data: selectedFeature.values_.data,
          etiqueta: selectedFeature.values_.data.name+' LOCK',
          geometry: selectedFeature.getGeometry()
        }));
      }
      else{
        if(selectedFeature.values_.data.on_use){
          SELECTEDsource.addFeature(new ol.Feature({
            type:'parkingSELECT-on_use',
            data: selectedFeature.values_.data,
            etiqueta: selectedFeature.values_.data.name,
            geometry: selectedFeature.getGeometry()
          }));
        }
        else{
          SELECTEDsource.addFeature(new ol.Feature({
            type:'parkingSELECT',
            data: selectedFeature.values_.data,
            etiqueta: selectedFeature.values_.data.name,
            geometry: selectedFeature.getGeometry()
          }));
        }
      }
      $('#selectedtitle').text(selectedFeature.values_.data.name);
      var there = ol.proj.transform([selectedFeature.values_.data.lng,selectedFeature.values_.data.lat], 'EPSG:4326', 'EPSG:3857')
      map.getView().animate({duration:500, center:there, zoom:17})

      opencontentfeature(selectedFeature);
      
    }
    else{

    }
    
  });
  
  if(selectedFeature == null){
    contentdrawer.open=false;
    SELECTEDsource.clear();
    here = evt.coordinate;
    lat = punto[1];
    lng = punto[0];
    point.setCoordinates(here);
    circle.setCenter(here);
    map.getView().animate({duration:500, center:here, zoom:17})
    loadDataFromServer();
  }

});

function clearbasicfeature(){
  datafromserver.clear();
  return true;
}



var select = null;  // ref to currently selected interaction

// select interaction working on "singleclick"
var selectSingleClick = new ol.interaction.Select();

// select interaction working on "click"
var selectClick = new ol.interaction.Select({
  condition: ol.events.condition.click
});

// select interaction working on "pointermove"
var selectPointerMove = new ol.interaction.Select({
  condition: ol.events.condition.pointerMove
});

var selectAltClick = new ol.interaction.Select({
  condition: function(mapBrowserEvent) {
    return ol.events.condition.click(mapBrowserEvent) &&
        ol.events.condition.altKeyOnly(mapBrowserEvent);
  }
});


map.on('pointermove', function(browserEvent) {
  // first clear any existing features in the overlay
  HL.clear();
  var pixel = browserEvent.pixel;
  // then for each feature at the mouse position ...
  map.forEachFeatureAtPixel(pixel, function(feature,) {
    
    if(feature.values_.type=="parking" || feature.values_.type=="parking-on_use"){
      label = feature.values_.data.name;
      HL.addFeature(new ol.Feature({
        type:'parkingHL',
        etiqueta: feature.values_.data.name,
        geometry: feature.getGeometry()
      }));
    }
    if(feature.values_.type=="parking-far"){
      label = feature.values_.data.name;
      HL.addFeature(new ol.Feature({
        type:'parkingHL-far',
        etiqueta: feature.values_.data.name,
        geometry: feature.getGeometry()
      }));
    }
    if(feature.values_.type=="parking-lock"){
      label = feature.values_.data.name;
      HL.addFeature(new ol.Feature({
        type:'parkingHL-lock',
        etiqueta: feature.values_.data.name,
        geometry: feature.getGeometry()
      }));
    }
  });
});



var prevzoom;
var zoom;

map.getView().on('propertychange', function(e) {
  switch (e.key) {
     case 'resolution':
     prevzoom = zoom;
     zoom = Math.round(map.getView().getZoom());
        if(zoom == 12 && prevzoom == 13){
          contentdrawer.open=false;
          loadDataFromServer();
          SELECTEDsource.clear();
        }
       break;
  }
});
