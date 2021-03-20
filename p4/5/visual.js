var w = window.innerWidth;
var h = window.innerHeight;

var historyLinks = [
	"https://supportcuanschutz.ucdenver.edu/2020/02/21/the-power-of-philanthropy-benefactors-celebrated-for-generosity/",
	"https://www.100andchange.org/",
	"https://www.sellingpower.com/2010/02/02/8094/venita-vancaspel"
];

var focus_node = null, highlight_node = null;

var text_center = false;

var min_score = 0;
var max_score = 1;

var highlight_color = "red";
var highlight_trans = 0.1;

var size = d3.scale.pow().exponent(1)
	.domain([1,100])
	.range([8,24]);
	
force = d3.layout.force()
	.linkDistance(60)
	.charge(-300)
	.size([w,h])
	.gravity(0.1);

var default_node_color = "#ccc";
var default_link_color = "#888";
var nominal_base_node_size = 8;
var nominal_text_size = 10;
var max_text_size = 24;
var nominal_stroke = 1;
var max_stroke = 4.5;
var max_base_node_size = 36;
var min_zoom = 0.1;
var max_zoom = 7;
var svg = d3.select("body").append("svg");
var zoom = d3.behavior.zoom().scaleExtent([min_zoom,max_zoom])
var g = svg.append("g");
svg.style("cursor","move");

d3.json("p4_5_scraped.json", function(error, graph) {

	var linkedByIndex = {};

	graph.edges.forEach(function(d) {
		linkedByIndex[d.source + "," + d.target] = true;
	});

	function isConnected(a, b) {
        return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
    }

	function hasConnections(a) {
		for (var property in linkedByIndex) {
				s = property.split(",");
				if ((s[0] == a.index || s[1] == a.index) && linkedByIndex[property]) 					return true;
		}
		return false;
	}

  	force
    	.nodes(graph.nodes)
    	.links(graph.edges)
    	.start();

  	var link = g.selectAll(".link")
    	.data(graph.edges)
    	.enter().append("line")
    	.attr("class", "link")
	  	.style("stroke-width",nominal_stroke)
	  	.style("stroke", default_link_color)


  	var node = g.selectAll(".node")
    	.data(graph.nodes)
    	.enter().append("g")
    	.attr("class", "node")
        .call(force.drag);


	var tocolor = "fill";
	var towhite = "stroke";


  	var circle = node.append("circle")
    	.style(tocolor, function(d, i) {
    	    if (graph.historyLinks.includes(d.name) && d.secondLevelDomain == 'org') {
    	        return "orange";
    	    }
			if(graph.historyLinks.includes(d.name)) {
            	return "red";
			}
            if(d.secondLevelDomain == 'org') {
            	return "yellow";
            }
            return default_node_color;
		})
                     
    	.attr("r", function(d, i) {
        	if(d.secondLevelDomain == 'org'){
            	return 10;
			}
           	return 5;
		})
		.style("stroke-width", nominal_stroke)
		.style(towhite, "white");


	var text = g.selectAll(".text")
		.data(graph.nodes)
		.enter().append("text")
		.attr("dy", ".35em")
		.style("font-size", nominal_text_size + "px")


	node.on("mouseover", function(d) {
			set_highlight(d);
		})
  		.on("mousedown", function(d) {   		
  			d3.event.stopPropagation();
  			focus_node = d;
			set_focus(d)
			if (highlight_node === null) 
				set_highlight(d);	
		})
		.on("mouseout", function(d) {
			exit_highlight();
		});


	d3.select(window).on("mouseup", function() {
		if (focus_node!==null) {
			focus_node = null;
			
			if (highlight_trans<1) {
				circle.style("opacity", 1);
	  			text.style("opacity", 1);
	  			link.style("opacity", 1);
			}
		}

		if (highlight_node === null) 
			exit_highlight();
		});

	function exit_highlight() {
		highlight_node = null;
		if (focus_node===null) {
			svg.style("cursor","move");
			circle.style("stroke", "white");
	 		text.style("font-weight", "normal")
     			.text( '\u2002');
	  		link.style("stroke", default_link_color);
		}
	}

	function set_focus(d) {
		if (highlight_trans<1)  {
    		circle.style("opacity", function(o) {
                return isConnected(d, o) ? 1 : highlight_trans;
            });

			text.style("opacity", function(o) {
                return isConnected(d, o) ? 1 : highlight_trans;
            });

            link.style("opacity", function(o) {
                return o.source.index == d.index || o.target.index == d.index ? 1 : highlight_trans;
            });
		}
	}


	function set_highlight(d) {
		svg.style("cursor","pointer");
		if (focus_node!==null) 
			d = focus_node;
			
		highlight_node = d;
		circle.style(towhite, function(o) {
                return isConnected(d, o) ? highlight_color : "white";
		});

		text.style("font-weight", function(o) {
			if (isConnected(d, o)) {
				if (d == o) {
                	return "bold";
            	} else {
                	return "normal";
                }text.style("background-color", function(o){
                		    return "yellow"; 
                		});
			} else {
            	return "normal";
            }
		});
		text.attr("dx", nominal_base_node_size)
        	.text(function(o) {
            	if (isConnected(d, o)) {
                	return '\u2002'+o.name;
                } else {
                	return '\u2002';
                }
			}
		);
		text.style("background-color", function(o){
				    return "yellow"; 
				});
      	link.style("stroke", function(o) {
			return o.source.index == d.index || o.target.index == d.index ? highlight_color : default_link_color;
		});
	}

	node.on("dblclick.zoom", function(d) {
		d3.event.stopPropagation();
		var dcx = (window.innerWidth/2-d.x*zoom.scale());
		var dcy = (window.innerHeight/2-d.y*zoom.scale());
		zoom.translate([dcx,dcy]);
 		g.attr("transform", "translate("+ dcx + "," + dcy  + ")scale(" + zoom.scale() + ")");
	});

	zoom.on("zoom", function() {
		g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
	});

	svg.call(zoom);

	resize();

	d3.select(window).on("resize", resize);

    var i = 0;
        
	force.on("tick", function() {

		node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
		text.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });

    	node.attr("cx", function(d) { return d.x; })
      		.attr("cy", function(d) { return d.y; });
        if (i < 300) {
            ++i;
        } else {
            force.stop();   
        }
	});
	

    function resize() {
		var width = window.innerWidth, height = window.innerHeight;
		svg.attr("width", width).attr("height", height);

		force.size([force.size()[0]+(width-w)/zoom.scale(),force.size()[1]+(height-h)/zoom.scale()]).resume();
    	w = width;
		h = height;
	}
});

function isNumber(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}
