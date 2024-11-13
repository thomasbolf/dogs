
fetch("http://localhost:5001/number_of_dogs").then(response => response.json()).then(data => {
    const numberOfDogs = document.getElementById("number-of-dogs");
    numberOfDogs.innerHTML = "Pets in shelters: " + data;
}
);



const svg = d3
    .select("#d3-container")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .style("display", "block")
    .style("margin", "0 auto")
    ;

const x = d3
  .scaleLinear()
  .domain([2.6, 75.1])
  .rangeRound([600, 860]);

const color = d3
  .scaleThreshold()
  .domain(d3.range(1, 5000, (5000) / 8))
  .range(d3.schemeReds[9]);



const tooltip = d3
  .select("body")
  .append("div")
  .attr("class", "tooltip")
  .attr("id", "tooltip")
  .style("opacity", 0);

const unemployment = d3.map();

const path = d3.geoPath();


Promise.all([
    d3.json("https://raw.githubusercontent.com/no-stack-dub-sack/testable-projects-fcc/master/src/data/choropleth_map/counties.json"),
    d3.csv("http://127.0.0.1:5001/counties") //dog data
]).then(([us, dogs]) => {
    ready(null, us, dogs);
}).catch(error => {
    console.error('Error loading data:', error);
});


function ready(error, us, dogs) {
    const dogData = new Map();
    dogs.forEach(d => {
      dogData.set(+d.county, +d.frequency); 
    });
    const fipsCounty = new Map();

    dogs.forEach(d => {
        fipsCounty.set(+d.county, d.name); 
        
    });

    var texasCounties = topojson.feature(us, us.objects.counties).features.filter(function(d) {
        return d.id >= 48001 && d.id <= 48999;
      });    
    const g = svg.append("g")
      .attr("transform", "scale(2)translate(-310,-325)rotate(-3)");
     g
    .append("g")
    .attr("class", "counties")
    .selectAll("path")
    .data(texasCounties)
    .enter()
    .append("path")
    .attr("class", "county")
    .attr("data-fips", d => d.id)
    .attr("fill", d => {
        console.log(d.id);
        const value = dogData.get(d.id);
        return value ? color(value) : "#ccc";
      })
    .attr("d", path)
    .on("mouseover", function (d) {

        d3.select(this).style("fill", "orange").transition().duration(200); 
        tooltip.transition().duration(200).style("opacity", 2);
        tooltip
          .html(
            fipsCounty.get(d.id) +
              "<br>" +
              dogData.get(d.id) +
              "<br>" +
              "pets in shelters" 
          )
          .style("font-size", "30px")
          .style("left", d3.event.pageX + 10 + "px")
          .style("top", d3.event.pageY - 28 + "px")
          .style("border-radius", "10px");
      })
      .on("mouseout", function() {

      d3.select(this)
        .style("fill", d => {
          const value = dogData.get(d.id);
          return value ? color(value) : "#ccc"; 
        });
        tooltip.transition().duration(500).style("opacity", 0);
      });
    
}
