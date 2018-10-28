<template>
  <div id="wrapper">
    <!-- <img id="logo" src="~@/assets/logo.png" alt="electron-vue"> -->
    <l-map ref="map" :zoom=13 :center="[ 36.23109, 37.99964]">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
          <l-geo-json
            :geojson="geojson1"
            :options="goptions"
            />
          <l-geo-json
            :geojson="geojson2"
            :options="goptions"
            />
    </l-map>
  </div>
</template>

<script>
  import { LMap, LTileLayer, LMarker, LGeoJson } from 'vue2-leaflet'
  import { InfoControl, ReferenceChart, ChoroplethLayer } from 'vue-choropleth'
  import L from 'leaflet'
  
  let dropIcon = L.icon({
    iconUrl: 'static/drop.png',
    iconSize: [32, 37],
    iconAnchor: [16, 37],
    popupAnchor: [0, -28]
  })

  let treeIcon = L.icon({
    iconUrl: 'static/tree.png',
    iconSize: [32, 37],
    iconAnchor: [16, 37],
    popupAnchor: [0, -28]
  })

  let urbanIcon = L.icon({
    iconUrl: 'static/shelter.png',
    iconSize: [32, 37],
    iconAnchor: [16, 37],
    popupAnchor: [0, -28]
  })

  let emptyIcon = L.icon({
    iconUrl: 'static/empty.png',
    iconSize: [32, 37],
    iconAnchor: [16, 37],
    popupAnchor: [0, -28]
  })

  function onEachFeatureFunction () {
    if (!this.enableTooltip) {
      return () => {}
    }
    return (feature, layer) => {
      layer.bindTooltip('<div>code:' + feature.properties.code + '</div><div>nom: ' + feature.properties.nom + '</div>', { permanent: false, sticky: true })
    }
  }

  function getPointToLayerFunction (feature, latlng) {
    let a = L.marker(latlng, {icon: dropIcon})
    let b = L.marker(latlng, {icon: treeIcon})
    let c = L.marker(latlng, {icon: urbanIcon})
    let d = L.marker(latlng, {icon: emptyIcon})
    let e = L.marker(latlng, {icon: emptyIcon})
    switch (feature.properties.values) {
      case 10:
        return a
      case 7:
        return b
      case 15:
        return b
      case 5:
        return c
      case 11:
        return d
      case 0:
        return e
      case 6:
        return b
      case 12:
        return b
      default:
        return b
    }
  }

  export default {
    name: 'landing-page',
    components: {
      LMap,
      LTileLayer,
      LMarker,
      LGeoJson,
      'l-info-control': InfoControl,
      'l-reference-chart': ReferenceChart,
      'l-choropleth-layer': ChoroplethLayer
    },
    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
      },
      geoLocation () {
        if (!navigator.geolocation) {
          console.log('Geolocation is not supported by your browser')
          return
        }
        let success = (position) => {
          console.log('success', position)
          this.$http.get('/map-resources', {params: {lat: position.coords.latitude, lng: position.coords.longitude}}).then(response => {
            // get body data
            this.geojson1 = response.data
          }, response => {
            // error callback
          })
        }
        let error = (err) => {
          console.log(err)
          console.log('error')
          this.$http.get('/map-resources/mcd15a2h', {params: {lat: 5.57225, lng: 32.63201}}).then(response => {
            // get body data
            this.geojson1 = response.data
          }, response => {
            // error callback
            console.log(response.error)
          })
        }
        navigator.geolocation.getCurrentPosition(success, error)
      }
    },
    computed: {
      styleFunction () {
        const fillColor = this.fillColor // important! need touch fillColor in computed for re-calculate when change fillColor
        return () => {
          return {
            weight: 2,
            color: '#ECEFF1',
            opacity: 1,
            fillColor: fillColor,
            fillOpacity: 1
          }
        }
      }
    },
    data: () => ({
      goptions: {
        onEachFeature: onEachFeatureFunction,
        pointToLayer: getPointToLayerFunction
      },
      geojson1: null,
      geojson2: null,
      fillColor: '#e4ce7f',
      map: null,
      url: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
    }),
    mounted () {
      // DO
      this.$nextTick(() => {
        this.map = this.$refs.map.mapObject // work as expected
        this.geoLocation()
      })
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');
  @import "~leaflet/dist/leaflet.css";

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  #wrapper {
    background:
      radial-gradient(
        ellipse at top left,
        rgba(255, 255, 255, 1) 40%,
        rgba(229, 229, 229, .9) 100%
      );
    height: 100vh;
    padding: 0;
    width: 100vw;
  }

  #logo {
    height: auto;
    margin-bottom: 20px;
    width: 420px;
  }

  main {
    display: flex;
    justify-content: space-between;
  }

  main > div { flex-basis: 50%; }

  .left-side {
    display: flex;
    flex-direction: column;
  }

  .welcome {
    color: #555;
    font-size: 23px;
    margin-bottom: 10px;
  }

  .title {
    color: #2c3e50;
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 6px;
  }

  .title.alt {
    font-size: 18px;
    margin-bottom: 10px;
  }

  .doc p {
    color: black;
    margin-bottom: 10px;
  }

  .doc button {
    font-size: .8em;
    cursor: pointer;
    outline: none;
    padding: 0.75em 2em;
    border-radius: 2em;
    display: inline-block;
    color: #fff;
    background-color: #4fc08d;
    transition: all 0.15s ease;
    box-sizing: border-box;
    border: 1px solid #4fc08d;
  }

  .doc button.alt {
    color: #42b983;
    background-color: transparent;
  }
</style>
