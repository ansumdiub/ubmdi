// get the data
var body = document.getElementsByTagName('body')[0];
document.getElementById('sidepanel').style.visibility = 'hidden';

//body.style.backgroundRepeat = "no-repeat";
d3.json("data.json", function(error, links) {
    // define the nodes
    var nodes = {};
    
    // Compute the distinct nodes from the links.
    links.forEach(function(link) {
        link.source = nodes[link.source] || 
            (nodes[link.source] = {name: link.source, area: link.value})
        link.target = nodes[link.target] || 
            (nodes[link.target] = {name: link.target, area: link.value})
    });
    
    // append path to fingerprint plots
    Array.from(nodes).forEach(function(n) {
        n[n.source]["fingerprint"] = "finger_prints_lo/" + n.name + "_lo.png";
    });
    
    var width = 1280,
        height = 720;
    
    var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([width, height])
        .linkDistance(50)
        .charge(-250)
        .on("tick", tick)
        .start();
    
    // Set the range
    var v = d3.scale.linear()
              .range([0, 100])
              .domain([0, d3.max(links, function(d) { return d.value; })]);
    
    var rScale = d3.scale.linear()
                   .domain([d3.min(force.nodes(), function(d) {
                       return d.area;
                   }), d3.max(force.nodes(), function(d) {
                       return d.area;
                   })])
                   .range([1, 25]);
                   
    var cScale = d3.scale.linear()
                   .domain([d3.max(force.nodes(), function(d) {
                       return d.area;
                   }), d3.min(force.nodes(), function(d) {
                       return d.area;
                   })])
                   .range([0, 1]);
                   
    materialInfo = d3.select("#materialInfo");
    
    var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);
    
    // build the arrow.
    svg.append("svg:defs").selectAll("marker")
       .data(["end"])      // Different link/path types can be defined here
       .enter().append("svg:marker")    // This section adds in the arrows
       .attr("id", String)
       .attr("viewBox", "0 -5 10 10")
       .attr("refX", 15)
       .attr("refY", -1.5)
       .attr("markerWidth", 6)
       .attr("markerHeight", 6)
       .attr("orient", "auto")
       .append("svg:path")
       .attr("d", "M0,-5L10,0L0,5");
    
    // add the links and the arrows
    var path = svg.append("svg:g").selectAll("path")
                  .data(force.links())
                  .enter().append("svg:path")
                  .attr("class", function(d) { return "link " + d.type; })
                  .attr("stroke", "gray");
                  
    console.log(force[0]);
    console.log(1);
    // define the nodes
    var node = svg.selectAll(".node")
                  .data(force.nodes())
                  .enter().append("g")
                  .attr("class", "node")
//                  .on("click", disp_info)
//                  .on("click", function(d) {disp_info(d); })
                  .on("dblclick", dblclick_event)
//                  .on("mouseover", function(d) {highlight(d, true, this); })
//                  .on("mouseout", function(d) {highlight(d, false, this); })
                  .call(force.drag);
    
    // add the nodes
    node.append("circle")
        .attr("r", function(d) { return rScale(d.area); })
        .attr("fill", function(d) {
            return d3.interpolateSpectral(cScale(d.area));
        });
    
    // add label to the nodes
    node.append("text")
        .attr("text-anchor", "start")
        .attr("dx", "10")
        .attr("dy", ".35em")
        .text(function(d) { return d.name; });
        
    // add the curvy lines
    function tick() {
        path.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
                
            return "M" + 
            d.source.x + "," + 
            d.source.y + "A" + 
            dr + "," + dr + " 0 0,1 " + 
            d.target.x + "," + d.target.y;
        });
        
        node.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    };
    
    function dblclick_event(d) {
        if (d.fixed == true) {
            d3.select(this)
              .select("circle")
              .attr("fill", function(d) {
                  return d3.interpolateSpectral(cScale(d.area));
              });
        d.fixed = false;
        } else {
            d3.select(this)
              .select("circle")
              .attr("fill", "#a0766c");
        d.fixed = true;
        }
    }
    
    function disp_info(d) {
        materialInfo.html(getMaterialInfo(d3.select(this), nodes))
                    .attr("class", "panel_on");
    }
    
    function getMaterialInfo(n, nodes) {
        info = '<div id="fingerprint">';
        if (n.fingerprint) {
            info += '<img class="fingerprint" height="300" src="' + n.fingerprint + '" title="' + n.name + '"/>';
        } else {
            info += '<div class=t style="float: right">' + n.name + '</div>';
        }
        return info;
    }

});