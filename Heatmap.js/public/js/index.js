
var HOUR_IN_MILLI = 1000 * 60 * 60 ;
var DAY_IN_MILLI = 1000 * 60 * 60 * 24;

var EuroCupAnimator = function(mapContainer,data){
  this.mapOptions =  {
    zoom: 12,
    center: new google.maps.LatLng(-0.182044, -78.466526),
    //center: new google.maps.LatLng(-0.187280, -78.471339),
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    disableDefaultUI: true,
    scrollwheel: true,
    draggable: true,
    navigationControl: true,
    mapTypeControl: false,
    scaleControl: true,
    zoomControl: true,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.DEFAULT,
      position: google.maps.ControlPosition.RIGHT_CENTER
    }
  };
  this.map = new google.maps.Map(mapContainer, this.mapOptions);

  this.data = data;
  this.heatmapOptions = {
    "radius": 10,// radius should be small ONLY if scaleRadius is true (or small radius is intended)
    "visible":true,
    "opacity": 40
  }

  this.heatmap = new HeatmapOverlay(this.map,this.heatmapOptions);
  this.dataLength = data.length - 1;


  this.dateRange = { start: data[0].created_at, end: data[data.length-1].created_at };
  this.dayRange = Math.ceil((this.dateRange.end - this.dateRange.start) / DAY_IN_MILLI);
  //this.dayRange = Math.ceil((this.dateRange.end - this.dateRange.start) / HOUR_IN_MILLI);

  this.isPaused = false;

   //calculate the number of days that elapse for each animation frame
  this.animationTimeMultiplier = 250000 * (this.dayRange / 365);
  //this.animationTimeMultiplier = 10000 * (this.dayRange / 24);

  this.visibleLifespan = Math.ceil(this.dayRange / 1);
    if(this.visibleLifespan < 10)
      this.visibleLifespan = 10;
    else if(this.visibleLifespan > 30)
      this.visibleLifespan = 30;

    this.visibleLifespan = this.visibleLifespan * HOUR_IN_MILLI;

  this.lowIndex = 0; 
  this.highIndex = 0;

  var $animationControlButton = $('#animation-control-button');
  //$animationControlButton.click(this.togglePause.bind(this));

  var me = this;

  google.maps.event.addListener(this.map, 'dragend', function() {
    if(me.isPaused)
      me.drawFrame(self.currentDate);
  });
  
  google.maps.event.addListener(this.map, 'zoom_changed', function() {
    var radiusMultiplier, zoom = me.map.getZoom();
    if(zoom > 10)
      radiusMultiplier = 2.6;
    else if(zoom < 9)
      radiusMultiplier = 1;
    else
      radiusMultiplier = 1.5;

    me.heatmap.heatmap.set('radius', zoom * radiusMultiplier);

    if(me.isPaused)
      me.drawFrame(self.currentDate);
  });

}

EuroCupAnimator.prototype.pause = function pause() {
  //this.$animationControl.removeClass('pause');
  this.$animationControl.addClass('play');

  this.isPaused = true;

  //draw markers
  if(this.showMarkers)
    this.addCrimeMarkers();
};

EuroCupAnimator.prototype.togglePause = function togglePause() {
  if(this.isPaused)
    this.resume();
  else
    this.pause();
};

EuroCupAnimator.prototype.updateIndexPositions = function updateIndexPositions(visibleThreshold, nextDate) {
  this.lowIndex = this.getNewIndexPosition(this.lowIndex, visibleThreshold, 0);

  if(this.highIndex < this.lowIndex)
    this.highIndex = this.lowIndex;

  this.highIndex = this.getNewIndexPosition(this.highIndex, nextDate, this.lowIndex);
}

EuroCupAnimator.prototype.getNewIndexPosition = function getNewIndexPosition(index, comparitorDate, indexMinimum) {
  //expand the index till it reaches the compairitor date
  while(index < this.dataLength) {
    if(this.data[index].created_at >= comparitorDate)
      break;

    index += 1;
  }

  //contract the index till it reaches the compairitor date
  while(index > indexMinimum) {
    if(this.data[index].created_at < comparitorDate)
      break;

    index -= 1;
  }

  return index;
};

EuroCupAnimator.prototype.drawFrame = function drawFrame(nextDate) {
    var visibleThreshold = this.currentDate - this.visibleLifespan;
    this.updateIndexPositions(visibleThreshold, nextDate);

    //if no removals to make then just add the crime points that are between the currentDate and the next Date and aren't filtered
    var currentData = this.getCurrentHeatmapData(this.lowIndex, this.highIndex, visibleThreshold);
    this.heatmap.setDataSet(currentData);
},

EuroCupAnimator.prototype.animate = function animate() {

  var now = new Date().getTime();

  if(!this.isPaused) {
    var nextDate = this.currentDate + ((now - this.lastDrawTime) * this.animationTimeMultiplier);

    this.drawFrame(nextDate);

    //increment currentDate to next date
    this.currentDate = nextDate;

    //update our current progress to match the current date
    //this.updateProgressBar();
  }

  this.lastDrawTime = now;

  if (this.highIndex < this.dataLength)
    window.requestAnimationFrame(this.animate.bind(this));
  else {
    //we are done
    this.isAnimating = false;
    this.pause();
  }
};

EuroCupAnimator.prototype.start = function start() {

  //set the current date to the first day if we are at the end of the animation
  if (this.highIndex >= this.dataLength || !this.currentDate)
    this.currentDate = this.dateRange.start;

  //reset our indexes
  this.lowIndex = 0;
  this.highIndex = 0;

  this.lastDrawTime = new Date().getTime();

  this.isAnimating = true;

  //start the animation
  this.animate();
}

EuroCupAnimator.prototype.getCurrentHeatmapData = function getCurrentHeatmapData(lowIndex, highIndex, visibleThreshold) {
  var currentData = this.data.slice(this.lowIndex, this.highIndex + 1);

  var crime, type, count, timeFromHighIndex, heatmapData = [];
  var currentTimeRange = this.currentDate - visibleThreshold;

  for(var i = currentData.length-1 ; i >= 0 ; i--) {
    crime = currentData[i];

    timeFromHighIndex = this.currentDate - crime.created_at;
    var x = timeFromHighIndex / currentTimeRange;
    count = Math.abs(4 * (x - Math.pow(x, 2))); //exponential curve for fade in/out
    heatmapData.push({lat : crime.lat, lng : crime.lng, count: count});
  }

  return {max: 2, data: heatmapData};
};
/*
EuroCupAnimator.prototype.pause = function pause() {
    //this.$animationControl.removeClass('pause');
    //this.$animationControl.addClass('play');
    this.isPaused = true;
    //draw markers
    if(this.showMarkers)
      this.addCrimeMarkers();
};*/


function getData(url){
  var tweets = [];

  $.getJSON(url,function(response){
    
    var docs = response.tweets;
    for(var i in docs){
      var location = docs[i].coordinates;
      tweets.push({
        lat: location.latitud,
        lng: location.longitud,
        created_at: getTimeStamp(docs[i].created_at),
      });
    }

    euroCupAnimator = new EuroCupAnimator(document.getElementById("map-canvas"),tweets);
      google.maps.event.addListenerOnce(euroCupAnimator.map, 
        'idle', 
        function() {
          //wait a bit for the user to get use to the map before we blow their mind with the animation
          window.setTimeout(
            function() {
              euroCupAnimator.start();
            }, 
          1000);
        }
      )
  });
}

function getTimeStamp(date_str){
  var now = new Date();
  var localOffset = now.getTimezoneOffset()*60000;//offset en mseg
  var date = new Date(Date.parse(date_str)).getTime()//obtiene el tiempo en mseg
 
  return date + localOffset;
}

var euroCupAnimator ;

function init(){

  window.requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
    window.webkitRequestAnimationFrame || window.msRequestAnimationFrame ||
    function(fn) {return setTimeout(fn, 1000 / 60);};

  getData("files/ecuador_terremoto.json");

}

window.addEventListener("load", init);