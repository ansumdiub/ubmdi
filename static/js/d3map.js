        let body = document.getElementsByTagName('body')[0];
        document.getElementById('sidePanel').style.visibility = 'hidden';
        let t = document.getElementsByTagName('body');
        let toggleDiv = undefined;
        let selectMaterial = undefined;
        let toggle = 0;
        body.style.backgroundRepeat = "no-repeat";

        d3.json("{% static 'data/data.json' %}", function(error, links) {
            // define the nodes
            let nodes = {};

            // Compute the distinct nodes from the links.
            links.forEach(function(link) {
                link.source = nodes[link.source] ||
                    (nodes[link.source] = {name:        link.source,
                                           lcd:         link.LCD[0],
                                           pld:         link.PLD[0],
                                           area:        link.area[0],
                                           density:     link.density[0],
                                           formula:     link.formula[0],
                                           space_group: link.space_group[0],
                                           fingerprint: "images/finger_prints_lo/" + link.source + "_lo.png"});

                link.target = nodes[link.target] ||
                    (nodes[link.target] = {name:        link.target,
                                           lcd:         link.LCD[1],
                                           pld:         link.PLD[1],
                                           area:        link.area[1],
                                           density:     link.density[1],
                                           formula:     link.formula[1],
                                           space_group: link.space_group[1],
                                           fingerprint: "images/finger_prints_lo/" + link.target + "_lo.png"})
            });

            let width = 750;
            let height = 750;

            let force = d3.layout.force()
                          .nodes(d3.values(nodes))
                          .links(links)
                          .size([width, height])
                        //.charge(-200)
                        //.linkDistance(50)
                          .charge(function(d) { return d._children ? -d.size / 100 : -30; })
                          .linkDistance(function(d) { return d.target._children ? 80 : 50; })
                          .on("tick", tick)
                          .start();

            let linkedByIndex = {};
            for (var i = 0; i < force.nodes().length; i++) {
                linkedByIndex[i + "," + i] = 1;
            }

            force.links().forEach(function(d) {
                linkedByIndex[d.source.index + "," + d.target.index] = 1;
            });

            // Set the range
            let v = d3.scale.linear()
                      .range([0, 100])
                      .domain([0, d3.max(links, function(d) { return d.value; })]);

            let rScale = d3.scale.linear()
                           .domain(d3.extent(force.nodes(), function(d) {
                               return d.area;
                           }))
                           .range([1, 25]);

            let cScale = d3.scale.linear()
                           .domain(d3.extent(force.nodes(), function(d) {
                               return d.area;
                           }))
                           .range([0, 1]);

            let materialInfo = d3.select("#materialInfo");
            let svg = d3.select("#main").append("svg")
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
            let path = svg.append("svg:g").selectAll("path")
                          .data(force.links())
                          .enter().append("svg:path")
                          .attr("class", function(d) { return "link " + d.type; })
                          .attr("stroke", "gray");

            // define the nodes
            let node = svg.selectAll(".node")
                          .data(force.nodes())
                          .enter().append("g")
                          .attr("class", "node")
                          .on("click", function(d) {disp_info(d); })
                          .on("dblclick", dblclick_event)
                          .on("mouseover", connectedNodes)
                          .on("mouseout", connectedNodes)
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
                        //dr = Math.sqrt(dx * dx + dy * dy);
                        dr = 0;

                    return "M" +
                    d.source.x + "," +
                    d.source.y + "A" +
                    dr + "," + dr + " 0 0,1 " +
                    d.target.x + "," + d.target.y;
                });

                node.attr("transform", function(d) {
                    return "translate(" + d.x + "," + d.y + ")";
                });
            }

            // double click event
            function dblclick_event(d) {
                if (d.fixed === 1) {
                    d3.select(this)
                      .select("circle")
                      .attr("fill", function(d) {
                          return d3.interpolateSpectral(cScale(d.area));
                      });
                d.fixed = 0;
                } else {
                    d3.select(this)
                      .select("circle")
                      .attr("fill", "#a0766c");
                d.fixed = 1;
                }
            }

            clearAndSelect = function (id) {
                toggleDiv('faq','off');
                toggleDiv('help','off');
                selectMaterial(id,true);
            };

            // mouse-out/out event: show details on side panel
            function neighboring(a, b) {
                return linkedByIndex[a.index + "," + b.index];
            }

            function connectedNodes() {
                d = d3.select(this).node().__data__;
                if (toggle === 0) {
                    node.style("opacity", function(n) {
                        return neighboring(d, n) || neighboring(n, d) ? 1 : 0.15;
                    });
                    toggle = 1;
                } else {
                    node.style("opacity", 1);
                    toggle = 0;
                }
            }

            // single click event: show details on side panel
            function disp_info(d) {
                //console.log(d);
                materialInfo.html(getMaterialInfo(d))
                            .attr("class", "panel_on");
            }

            function getMaterialInfo(d) {
                var info = '<div id="cover">';
                info += '<img src="{% static 'images/Close.svg' %}" class="action" style="top:5px;right:5px;width:25px;height:25px;" title="close panel" onClick="toggleDiv(\'materialInfo\');"/>';
                if (d.fingerprint) {
                    $.ajax({
                        // url: this.actions,
                        url: "ajax/add/", // the endpoint
                        type: "POST", // http method
                        data: {mof_name: d.name}, // data sent with the post request

                        // handle a successful response
                        success: function(mof_png) {
                            // console.log(json); // log the returned json to the console
                            console.log("success"); // another sanity check

                            // console.log(info)
                            $('.card-body').empty();
                            $('.list-group').empty();
                            $('#fingerprint').attr("src", "data:image/png;base64," + mof_png);
                            },

                        // handle a non-successful response
                        error: function(xhr, errmsg, err) {
                            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                            }
                    });
                    info += '</div>';
                    console.log(d.name);
                }

                info += '<div class=f><span class=l>' + d.name + '<span></div>';
                if (d.lcd) {
                   info += '<div class=f><span class=l>LCD</span>: <span class=d>'
                    + d.lcd + ' <span>&#8491;</span>' + '</span></div>';
                }
                if (d.pld) {
                    info += '<div class=f><span class=l>PLD</span>: <span class=d>'
                    + d.pld + ' <span>&#8491;</span>' + '</span></div>';
                }
                if (d.area) {
                    info += '<div class=f><span class=l>Accessible Surface Area</span>: <span class=d>'
                    + d.area + ' m<sup>2</sup>/g' + '</span></div>';
                }
                if (d.density) {
                    info += '<div class=f><span class=l>Density</span>: <span class=d>'
                    + d.density + ' g<sup>3</sup>/m' + '</span></div>';
                }
                if (d.formula) {
                    info += '<div class=f><span class=l>Formula</span>: <span class=d>'
                    + d.formula + '</span></div>';
                }
                if (d.space_group) {
                    info += '<div class=f><span class=l>Space Group</span>: <span class=d>'
                    + d.space_group + '</span></div>';
                }
                // link to CSD
                info += '<div class=f><span class=l>Link to CCDC library</span>: <span class=d>'
                     + '<a href="https://www.ccdc.cam.ac.uk/structures/Search?Ccdcid=' + d.name + '"'
                     + '>Ref to details in CCDC</a></span></div>';
                // Similar Materials
                info += '<div class=f><span class=l>Related to</span>: ';
                for (var i = 0; i < force.nodes().length; i++) {
                    if (linkedByIndex[d.index + "," + i] === 1 || linkedByIndex[i + "," + d.index] === 1) {
                        info += '[<a href="javascript:void(0);" onclick="selectMaterial('
                        + i + ',true);">' + force.nodes()[i].name + '</a>]';
                    }
                }

                info += '</div>';
                return info;

            }

            /*lcd, pld, area, density, formula, space_group, vol_frac, finger_print*/

            toggleDiv = function(id, status) {
                d = d3.select('div#'+id);
                if (status === undefined) {
                    status = d.attr('class') === 'panel_on' ? 'off' : 'on';
                }
                d.attr('class', 'panel_' + status);
                return false;
            }
        });