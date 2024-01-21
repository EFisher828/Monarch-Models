const map = new maplibregl.Map({
  container: 'map',
  style: './monarch_style.json',
  zoom: 3.5,
  center: [-95.901,37.852],
  maxBounds: [[-143.0,16.5],[-50.2,56.8]],
  pitchWithRotate: false,
  dragRotate: false,
});

map.addControl(new mapboxgl.FullscreenControl({container: document.querySelector('map')}));

map.addControl(new mapboxgl.GeolocateControl({
  positionOptions: {
    enableHighAccuracy: false
    },
  trackUserLocation: true,
  showUserHeading: true
}));

// Initialize an empty array to store the date-time strings
const dateTimes = [];

// Set the start and end date
const startDate = new Date('2024-01-21T12:00:00');
const endDate = new Date('2024-02-10T23:00:00');

// Loop through the hours between start and end dates
let currentDate = startDate;
while (currentDate <= endDate) {
  // Format the current date as 'YYYYMMDDHH'
  const year = currentDate.getFullYear();
  const month = (currentDate.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-based
  const day = currentDate.getDate().toString().padStart(2, '0');
  const hour = currentDate.getHours().toString().padStart(2, '0');

  // Add the formatted date-time string to the array
  dateTimes.push(`${year}${month}${day}${hour}`);

  // Increment the current date by 1 hour
  currentDate = new Date(currentDate.getTime() + (60 * 60 * 6000));
}

// Initialize an empty array to store the formatted date-time strings in Eastern Time
const formattedDateTimesET = [];

// Loop through the dateTimes array and format each date-time string in Eastern Time
dateTimes.forEach(dateTime => {
  // Parse the 'YYYYMMDDHH' string into a Date object
  const year = dateTime.substring(0, 4);
  const month = dateTime.substring(4, 6) - 1; // Months are zero-based
  const day = dateTime.substring(6, 8);
  const hour = dateTime.substring(8, 10);

  // Create a Date object in UTC
  const formattedDateUTC = new Date(Date.UTC(year, month, day, hour));

  // Format the date as '7PM March 13, 1993' in Eastern Time
  // Format the date as '09 PM March 13, 1993' in Eastern Time
  const options = { hour: '2-digit', hour12: true, month: 'short', day: '2-digit', year: 'numeric' };
  const formattedStringET = formattedDateUTC.toLocaleString('en-US', { timeZone: 'America/New_York', ...options });

  // Extract hours and AM/PM and format them as '09 PM'
  const [time, ampm, rest] = formattedStringET.split(' ');
  const formattedTimeString = time + ' ' + ampm;

  // Reconstruct the final date string
  const finalFormattedString = formattedTimeString + ' ' + rest;

  // Add the formatted string to the array
  formattedDateTimesET.push(formattedStringET + ' EST');
});

let snow_legend = './snow-legend.png'
let precp_type_legend = './precip-type-legend.png'
let precip_legend = './precip-legend.png'
let wind_legend = './wind-legend.png'
let temp_legend = './temp-legend.png'

let variable_dict = {
  'Snow': ['Accumulated Snowfall (in)','./snow-legend.png'],
  'ptype': ['Precipitation Type & Rate','./precip-type-legend.png'],
  'Wind': ['Wind Speed (kt)','wind-legend.png'],
  'Temp': ['Temperature (°F)','temp-legend.png'],
  'Wind-Chill': ['Wind Chill (°F)','temp-legend.png'],
  'Precip': ['Accumulated Precipitation','./precip-legend.png']
}

let variable = 'ptype'
map.on('load', function() {
  // Add a GeoJSON source to the map
  map.addSource('coastlines', {
    type: 'geojson',
    data: './GeoJSONs/coastlines.geojson' // Path to your GeoJSON file
  });

  // Add a layer to display the GeoJSON data
  map.addLayer({
    id: 'coastlines',
    type: 'line', // Change the type based on your GeoJSON geometry type
    source: 'coastlines',
    paint: {
      'line-color': 'hsl(240, 18%, 29%)',
      'line-width': 0.5
    }
  },"label_airport");

  var detailsElement = document.querySelector('.mapboxgl-compact-show');
  if (detailsElement) {
        // Remove the 'open' attribute
        detailsElement.removeAttribute('open');

        // Remove the 'maplibregl-compact-show' and 'mapboxgl-compact-show' classes
        detailsElement.classList.remove('maplibregl-compact-show', 'mapboxgl-compact-show');
    }

  // Add zoom and rotation controls to the map.
  map.addControl(new maplibregl.NavigationControl(), 'top-right')

  // Initialize the image source
  map.addSource('image-source', {
    'type': 'image',
    'url': `./Exports/GFS/ptype/${dateTimes[0]}.png`, // Initial date
    'coordinates': [
        [-143.0, 56.8],
        [-50.2, 56.8],
        [-50.2, 16.5],
        [-143.0, 16.5]
    ],
  });

  map.addLayer({
    'id': 'image-layer',
    'type': 'raster',
    'source': 'image-source',
    'paint': {
      'raster-opacity': 0.95,
      'raster-fade-duration': 0,
      'raster-resampling': "nearest"
    }
  },'building');

  document.getElementById('dateSlider').addEventListener('input', function(event) {
    let endFrame = event.target.max
    let selectedFrame = event.target.value
    let currentDate = document.getElementById('currentDate');

    map.getSource('image-source').updateImage({ url: `./Exports/GFS/${variable}/${dateTimes[selectedFrame]}.png` });
    currentDate.textContent = formattedDateTimesET[selectedFrame];
  });

  const snow = document.getElementById('snowfall')
  const precipType = document.getElementById('preciptype')
  const precip = document.getElementById('precip')
  //const wind = document.getElementById('wind')
  //const temp = document.getElementById('temp')
  //const windChill = document.getElementById('windchill')

  snow.addEventListener('click', function() {
    variable = 'Snow'
    let selectedFrame = document.getElementById('dateSlider').value
    map.getSource('image-source').updateImage({ url: `./Exports/GFS/${variable}/${dateTimes[selectedFrame]}.png` });
    currentDate.textContent = formattedDateTimesET[selectedFrame];
    document.getElementById('legend').src = snow_legend
  });

  precipType.addEventListener('click', function() {
    variable = 'ptype'
    let selectedFrame = document.getElementById('dateSlider').value
    map.getSource('image-source').updateImage({ url: `./Exports/GFS/${variable}/${dateTimes[selectedFrame]}.png` });
    currentDate.textContent = formattedDateTimesET[selectedFrame];
    document.getElementById('legend').src = precp_type_legend
  })

  precip.addEventListener('click', function() {
    variable = 'Precip'
    let selectedFrame = document.getElementById('dateSlider').value
    map.getSource('image-source').updateImage({ url: `./Exports/GFS/${variable}/${dateTimes[selectedFrame]}.png` });
    currentDate.textContent = formattedDateTimesET[selectedFrame];
    document.getElementById('legend').src = precip_legend
  })

  /*wind.addEventListener('click', function() {
    variable = 'Wind'
    let selectedFrame = document.getElementById('dateSlider').value
    map.getSource('image-source').updateImage({ url: `./Exports/${variable}/${dateTimes[selectedFrame]}.png` });
    currentDate.textContent = formattedDateTimesET[selectedFrame];
    document.getElementById('legend').src = wind_legend
  })

  temp.addEventListener('click', function() {
    variable = 'Temp'
    let selectedFrame = document.getElementById('dateSlider').value
    map.getSource('image-source').updateImage({ url: `./Exports/${variable}/${dateTimes[selectedFrame]}.png` });
    currentDate.textContent = formattedDateTimesET[selectedFrame];
    document.getElementById('legend').src = temp_legend
  })

  windChill.addEventListener('click', function() {
    variable = 'Wind-Chill'
    let selectedFrame = document.getElementById('dateSlider').value
    map.getSource('image-source').updateImage({ url: `./Exports/${variable}/${dateTimes[selectedFrame]}.png` });
    currentDate.textContent = formattedDateTimesET[selectedFrame];
    document.getElementById('legend').src = temp_legend
  })*/

  const checkboxes = document.querySelectorAll('input[type="checkbox"]');

  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      checkboxes.forEach(otherCheckbox => {
        if (otherCheckbox !== checkbox) {
          otherCheckbox.checked = false;
        }
      });
    });
  });
});

function captureHighResolutionImage(map, callback) {
  let selectedFrame = document.getElementById('dateSlider').value;
  console.log(variable)

  // Define the dimensions of the canvas, including whitespace
  const canvasWidth = 1920; // HD width
  const canvasHeight = 1280; // HD height
  const whitespaceSizeTop = 40; // Adjust the top whitespace size as needed
  let whitespaceSizeBottom;
  if (variable == 'Temp') {
    whitespaceSizeBottom = 120 // Adjust the bottom whitespace size as needed
  } else if (variable == 'Precip') {
    whitespaceSizeBottom = 100
  } else {
    whitespaceSizeBottom = 140
  }/*else if (document.getElementById('legend').src != './temp-legend.png') {
    whitespaceSizeBottom = 90
  }*/

  // Create an offscreen canvas with the new dimensions
  const offscreenCanvas = document.createElement('canvas');
  offscreenCanvas.width = canvasWidth;
  offscreenCanvas.height = canvasHeight;

  // Get the rendering context of the offscreen canvas
  const offscreenContext = offscreenCanvas.getContext('2d');

  // Fill the entire canvas with a background color (white in this example)
  offscreenContext.fillStyle = 'white';
  offscreenContext.fillRect(0, 0, canvasWidth, canvasHeight);

  // Calculate the position to center the map
  const mapX = whitespaceSizeTop;
  const mapY = whitespaceSizeTop;
  const mapWidth = canvasWidth - 2 * whitespaceSizeTop;
  const mapHeight = canvasHeight - whitespaceSizeTop - whitespaceSizeBottom;

  // Render the map within the canvas
  offscreenContext.drawImage(map.getCanvas(), mapX, mapY, mapWidth, mapHeight);
  console.log(variable_dict)
  // Add text inside the top whitespace
  offscreenContext.fillStyle = 'black'; // Text color
  offscreenContext.font = 'bold 24px Arial'; // Font size and style
  offscreenContext.fillText(formattedDateTimesET[selectedFrame], mapWidth - 240, 32); // Adjust the text position
  offscreenContext.fillText(variable_dict[variable][0], 40, 32);

  // Load and draw an image at the bottom of the canvas
  const image = new Image();
  image.src = variable_dict[variable][1]; // Replace with the URL of your image
  image.onload = () => {
    const imageWidth = canvasWidth * 0.9; // 90% of canvas width
    const imageHeight = imageWidth * (image.height / image.width);
    const imageX = (canvasWidth - imageWidth) / 2;
    const imageY = canvasHeight - imageHeight - whitespaceSizeBottom;
    offscreenContext.drawImage(image, imageX, canvasHeight - imageHeight - 10, imageWidth, imageHeight);

    // Convert the canvas to a data URL and invoke the callback
    const dataURL = offscreenCanvas.toDataURL('image/png');
    callback(dataURL);
  };
}

const sliderButtonOff = document.getElementById('hideSlider')

sliderButtonOff.addEventListener('click', () => {
  document.getElementById('dateSlider').style.display = 'none'
})

const sliderButtonOn = document.getElementById('showSlider')

sliderButtonOn.addEventListener('click', () => {
  document.getElementById('dateSlider').style.display = 'block'
})

// Add a click event listener to the button
document.getElementById('saveMapButton').addEventListener('click', () => {
  // Get the map container and create a canvas element
  const mapContainer = document.getElementById('map');
  const canvas = document.createElement('canvas');

  // Set the canvas dimensions to match the map's dimensions
  canvas.width = mapContainer.offsetWidth;
  canvas.height = mapContainer.offsetHeight;

  // Get a 2D rendering context for the canvas
  const context = canvas.getContext('2d');

  // Draw the map onto the canvas
  map.once('render', () => {
    context.drawImage(map.getCanvas(), 0, 0);

    // Capture a higher resolution image (4K)
    captureHighResolutionImage(map, (highResDataURL) => {
      // Create an anchor element with the image data URL and trigger a download
      const downloadLink = document.createElement('a');
      downloadLink.href = highResDataURL;
      downloadLink.download = './saved-model-output.png'; // Set the file name
      downloadLink.click();
    });
  });

  // Trigger a map render
  map.jumpTo({ duration: 0 });
});
