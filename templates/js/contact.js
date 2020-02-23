$('#select-beast').selectize({
  create: true,
  sortField: {
    field: 'text',
    direction: 'asc'
  },
  dropdownParent: 'body'
});
function initialize() {
  var mapOptions = {
    zoom: 7,
    center: new google.maps.LatLng(28.9913522, -85.4145614),
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    scrollwheel: false,
    navigationControl: false,
    mapTypeControl: false,
    scaleControl: false
  };

  var styles = [ {
    stylers: [
      {saturation: -100}
    ]
  } ];

  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  var mapType = new google.maps.StyledMapType(styles, {name: "Grayscale"});
  map.mapTypes.set('grayMap', mapType);
  map.setMapTypeId('grayMap');

  // var myLatlng = new google.maps.LatLng(28.541638, -81.368941);
  var myLatlng = new google.maps.LatLng(28.5556405, -81.3775403);

  var imgWebCorpCo = {
    url: '/_resources/images/content/marker.png',
    size: new google.maps.Size(244, 182),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(24, 54)
  };

  var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title: 'WebCorpCo',
    icon: imgWebCorpCo
  });
}

function loadScript() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  //script.src = 'http://maps.google.com/maps/api/js?sensor=false';
  script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAvNegdMhrApxE5o7jlPEHGS-gk03rxgUc&sensor=false&callback=initialize';
  document.body.appendChild(script);
}

window.onload = loadScript;