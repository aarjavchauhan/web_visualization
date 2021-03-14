fetch("results.json")
    .then(response => response.json())
    .then(json => {
        var edgesArray = [];
        json.edges.forEach((element, index) => {
            edgesArray.push(
                { from: element.source, to: element.target }
            );
        });

        var nodesArray = [];
        json.nodes.forEach((element, index) => {
            nodesArray.push(
                { id: index, label: element.name }
            );
        });

        // create a network
        var container = document.getElementById("mynetwork");
        var data = {
            nodes: nodesArray,
            edges: edgesArray,
        };
        var options = {
            nodes: {
                shape: "dot",
                scaling: {
                    min: 10,
                    max: 30
                }
            },
            physics: {
                enabled: true
            }
        };
        var network = new vis.Network(container, data, options);
    });
