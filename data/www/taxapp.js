// *** FL Tax App JS File ***
// ** OpenLayers JS ***

//Declare layers
var map, vector_layer;
var SELECT_FROM_CLICK = true;

function init(){
    //Create map
    map = new OpenLayers.Map('map_element',{
        // Empty controls
        controls:[]
    });
    //Google streets base layer
    var google_streets = new OpenLayers.Layer.Google(
        "Google Streets",
        {}
    );
    //*** Vector Layer ***
    //Create format obj
    var vector_format = new OpenLayers.Format.GeoJSON({});
    //Create protocol obj
    var vector_protocol = new OpenLayers.Protocol.HTTP({
        url: "/staticfiles/county_boundary.json",
        format: vector_format
    });
    //Create array of strategy obj
    var vector_strategies = [new OpenLayers.Strategy.Fixed()];
    //Create vector layer with F,P,S
    var vector_layer = new OpenLayers.Layer.Vector('County Boundry', {
        protocol: vector_protocol,
        strategies: vector_strategies
    });
    //*** End Vector Layer Code

    //Add Layers
    map.addLayers([
        google_streets,
        vector_layer
    ]);

    //*** Feature Code ***
    var select_feature_control = new OpenLayers.Control.SelectFeature(
        vector_layer,
        {
            multiple: false,
            toggle: true,
            multipleKey: 'shiftKey',
            toggleKey: 'altKey'
        }
    );
    map.addControl(select_feature_control);
    select_feature_control.activate();

    function selected_feature(event){
        if(SELECT_FROM_CLICK === true){
            var county_name = event.feature.attributes.NAME;
            update_left_content(county_name);

            xmlhttp = new XMLHttpRequest();

            xmlhttp.onreadystatechange = function(){
                if(xmlhttp.readyState == 4 && xmlhttp.status==200) {
                    update_left_content(county_name,xmlhttp.responseText);
                }
                else if(xmlhttp.status == 500){
                    document.getElementById('left_content').innerHTML = '<br />Error Occured';
                }
            }

            xmlhttp.open('GET','/get_county/' + county_name + '/', true);
            xmlhttp.send();
        }
        SELECT_FROM_CLICK = true;
    }

    vector_layer.events.register('featureselected', this, selected_feature);
    // Center Load
    if(!map.getCenter()){
        map.setCenter(
            new OpenLayers.LonLat(
                -83.28173828125,
                27.306640625).transform(
                    new OpenLayers.Projection('EPSG:4326'),
                    new OpenLayers.Projection('EPSG:900913')
                ),
        6);
    }
}

//*** Function - Update Left Data Upon Clicking County Vector Layer ***
function update_left_content(county, tax_rate){
    if(county === undefined){
        return null;
    }
    if(tax_rate === undefined){
        var tax_rate = undefined;
    }
    document.getElementById('left_content').innerHTML = '<br /><strong>County:</strong>' + county;
    if(tax_rate !== undefined){
        document.getElementById('left_content').innerHTML += '<br /><strong>Tax Rate:</strong>' + tax_rate;
    }
}

//*** Function - Update Right Vector Layer When Sucessful Query Results ***
function highlight_feature(county){
    for(i=0;i < map.layers[1].features.length;i++){
        if(map.layers[1].features[i].attributes.NAME === county){
            SELECT_FROM_CLICK = false;
            map.controls[0].select(map.layers[1].features[i]);
            return true;
        }
    }
    return false;
}
